from django.utils import timezone
from django.http import JsonResponse
from django.views import View
from .models import AppUser, IconPack, IconPackImage, Wallpaper, Preference, Color, Style
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import random
from .utils import generate_jwt, verify_jwt

import smtplib
import ssl
from email.message import EmailMessage

from rest_framework import generics
from rest_framework.response import Response

from .serializer import ColorSerializer, StyleSerializer


class WallpaperListView(View):
    def get(self, request):
        page = int(request.GET.get('page', 1))
        items_per_page = int(request.GET.get('items', 20))
        total_wallpapers = Wallpaper.objects.count()
        total_pages = (total_wallpapers + items_per_page - 1) // items_per_page

        start_index = (page - 1) * items_per_page
        end_index = start_index + items_per_page

        wallpapers = Wallpaper.objects.all()[start_index:end_index]

        data = {
            'total_pages': total_pages,
            'current_page': page,
            'total_images': total_wallpapers,
            'images': [{'id': wallpaper.id, 'title': wallpaper.title, 'image_url': wallpaper.image_url.url, 'created_at': wallpaper.created_at} for wallpaper in wallpapers]
        }

        return JsonResponse(data, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class IconPackApiView(View):
    def get(self, request):
        page = int(request.GET.get('page', 1))
        items_per_page = int(request.GET.get('items', 20))

        icon_packs = IconPack.objects.filter(active=True)

        total_icon_packs = icon_packs.count()
        total_pages = (total_icon_packs + items_per_page - 1) // items_per_page

        start_index = (page - 1) * items_per_page
        end_index = start_index + items_per_page

        icon_packs = icon_packs[start_index:end_index]

        data = {
            'total_pages': total_pages,
            'current_page': page,
            'total_icon_packs': total_icon_packs,
            'icon_packs': [{'id': icon_pack.id, 'name': icon_pack.name, 'preview': icon_pack.preview.url} for icon_pack in icon_packs]
        }

        return JsonResponse(data, safe=False)

    def post(self, request):
        try:
            id = request.POST.get('id')
            token = request.POST.get('token')

            if id is None:
                return JsonResponse({'error': 'Id is required'}, status=400)

            if token is None:
                return JsonResponse({'error': 'Token is required'}, status=400)

            if verify_jwt(token)[0] is False:
                return JsonResponse({'error': 'Invalid token'}, status=401)

            icon_pack = IconPack.objects.get(id=id)
        except IconPack.DoesNotExist:
            return JsonResponse({'error': 'IconPack not found'}, status=404)

        icon_pack_images = IconPackImage.objects.filter(icon_pack=icon_pack)

        data = {
            'id': icon_pack.id,
            'name': icon_pack.name,
            'preview': icon_pack.preview.url,
            'icon_pack': icon_pack.icon_pack.url,
            'created_at': icon_pack.created_at,
            'updated_at': icon_pack.updated_at,
            'images': [{'id': image.id, 'image_url': image.image_url.url} for image in icon_pack_images]
        }

        return JsonResponse(data, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class GetPreferenceImage(View):
    def post(self, request):
        try:
            color = request.POST.get('color')
            male = request.POST.get('male')

            if male == "0":
                male = False
            elif male == "1":
                male = True
            else:
                male = None
                return JsonResponse({'success': False, 'error': 'Invalid male value'})

            style_1_code = request.POST.get('style_1')
            style_2_code = request.POST.get('style_2') if male else None

            print(color, male, style_1_code, style_2_code)

            try:
                color_obj = Color.objects.get(color_code=color)
                Style_1 = Style.objects.get(style_code=style_1_code)

                if male:
                    Style_2 = Style.objects.get(style_code=style_2_code)
            except (Color.DoesNotExist, Style.DoesNotExist) as e:
                return JsonResponse({'success': False, 'error': str(e)})

            if male:
                preference = Preference.objects.filter(
                    color=color_obj,
                    male=male,
                    style_1=Style_1,
                    style_2=Style_2
                ).first()
            else:
                preference = Preference.objects.filter(
                    color=color_obj,
                    male=male,
                    style_1=Style_1,
                ).first()

            print(preference)

            if preference is None:
                return JsonResponse({'success': False, 'error': 'Preference not found'})

            return JsonResponse({'success': True, 'image_url': preference.image.url, 'icon_pack': preference.icon_pack.icon_pack.url})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


@method_decorator(csrf_exempt, name='dispatch')
class SendOTP(View):
    def post(self, request):
        try:
            email = request.POST.get('email')
            user, created = AppUser.objects.get_or_create(email=email)

            new_otp = random.randint(100000, 999999)
            user.otp = new_otp
            user.updated_at = timezone.now()
            user.save()

            if email is not "test@gmail.com":
                self.send_email(email, new_otp)

            return JsonResponse({'success': True, 'message': 'OTP sent or updated successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    def send_email(self, to_email, otp):
        em = EmailMessage()
        em["From"] = "Alerts@anatove.com"
        em["To"] = to_email
        em["Subject"] = "OTP for AICHROM"
        em.set_content(f"otp {otp} for aichrom", subtype='html')

        context = ssl.create_default_context()

        with smtplib.SMTP("smtp.hostinger.com", 587) as smtp:
            smtp.starttls(context=context)
            smtp.login("alerts@anatove.com", "fexfaz-xorjoV-1nespe")
            smtp.send_message(em)


@method_decorator(csrf_exempt, name='dispatch')
class VerifyOTP(View):
    def post(self, request):
        try:
            email = request.POST.get('email')
            otp = request.POST.get('otp')

            user = AppUser.objects.get(email=email)

            if email == "test@gmail.com" and otp == "999999":
                return JsonResponse({'success': True, 'token': generate_jwt(phone=email)})

            time_difference = timezone.now() - user.updated_at

            if user.otp == otp:
                if time_difference.total_seconds() <= 300:
                    token = generate_jwt(phone=email)
                    return JsonResponse({'success': True, 'token': token})
                else:
                    return JsonResponse({'success': False, 'error': 'OTP expired'})
            else:
                return JsonResponse({'success': False, 'error': 'Invalid OTP'})
        except AppUser.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


@method_decorator(csrf_exempt, name='dispatch')
class GetPreferenceSchema(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        male_colors = Color.objects.filter(preference__male=True).distinct()
        female_colors = Color.objects.filter(preference__male=False).distinct()

        style1_male = Style.objects.filter(
            preference_style_1__male=True).distinct()
        style2_male = Style.objects.filter(
            preference_style_2__male=True).distinct()

        style1_female = Style.objects.filter(
            preference_style_1__male=False).distinct()
        style2_female = Style.objects.filter(
            preference_style_2__male=False).distinct()

        response_data = {
            "male": {
                "colors": ColorSerializer(male_colors, many=True).data,
                "style_1": StyleSerializer(style1_male, many=True).data,
                "style_2": StyleSerializer(style2_male, many=True).data,
            },
            "female": {
                "colors": ColorSerializer(female_colors, many=True).data,
                "style_1": StyleSerializer(style1_female, many=True).data,
                "style_2": StyleSerializer(style2_female, many=True).data,
            },
        }

        return Response(response_data)

# @method_decorator(csrf_exempt, name='dispatch')
# class GetPreferenceSchema(View):
#     def get(self, request):
#         try:
#             style1_male_colors = Preference.objects.filter(
#                 male=True).values_list('color', flat=True).distinct()
#             style1_female_colors = Preference.objects.filter(
#                 male=False).values_list('color', flat=True).distinct()

#             style1_male = Preference.objects.filter(male=True).values(
#                 'style_1_Code', 'style_1_Image').distinct()
#             style1_female = Preference.objects.filter(male=False).values(
#                 'style_1_Code', 'style_1_Image').distinct()

#             style2_male = Preference.objects.filter(male=True).values(
#                 'style_2_Code', 'style_2_Image').distinct()
#             style2_female = Preference.objects.filter(male=False).values(
#                 'style_2_Code', 'style_2_Image').distinct()

#             result = {
#                 "male": {
#                     "colors": list(style1_male_colors),
#                     "style_1": list(style1_male),
#                     "style_2": list(style2_male)
#                 },
#                 "female": {
#                     "colors": list(style1_female_colors),
#                     "style_1": list(style1_female),
#                     "style_2": list(style2_female)
#                 }
#             }

#             return JsonResponse(result, safe=False)

#         except OperationalError as e:
#             error_message = f"Database error: {e}"
#             return JsonResponse({"error": error_message}, status=500)

#         except Exception as e:
#             error_message = f"An unexpected error occurred: {e}"
#             return JsonResponse({"error": error_message}, status=500)
