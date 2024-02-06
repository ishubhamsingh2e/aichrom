from django.utils import timezone
from django.http import JsonResponse
from django.views import View
from .models import AppUser, IconPack, IconPackImage, Wallpaper, Preference
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import random
from .utils import generate_jwt, verify_jwt

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

        total_icon_packs = IconPack.objects.count()
        total_pages = (total_icon_packs + items_per_page - 1) // items_per_page

        start_index = (page - 1) * items_per_page
        end_index = start_index + items_per_page

        icon_packs = IconPack.objects.all()[start_index:end_index]

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
            male = bool(request.POST.get('male'))
            style_1_code = request.POST.get('style_1')
            style_2_code = request.POST.get('style_2')

            preference = Preference.objects.get(
                color=color,
                male=male,
                style_1_Code=style_1_code,
                style_2_Code=style_2_code
            )

            try : icon_pack = IconPack.objects.get(id=preference.id).icon_pack
            except: icon_pack = None

            return JsonResponse({'success': True, 'image_url': preference.image.url, 'icon_pack': icon_pack.url})
        except Preference.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Preference not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


@method_decorator(csrf_exempt, name='dispatch')
class SendOTP(View):
    def post(self, request):
        try:
            phone = request.POST.get('phone')
            user, created = AppUser.objects.get_or_create(phone=phone)

            new_otp = random.randint(100000, 999999)
            user.otp = new_otp
            user.updated_at = timezone.now()
            user.save()

            return JsonResponse({'success': True, 'message': 'OTP sent or updated successfully', 'otp': new_otp})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


@method_decorator(csrf_exempt, name='dispatch')
class VerifyOTP(View):
    def post(self, request):
        try:
            phone = request.POST.get('phone')
            otp = request.POST.get('otp')

            user = AppUser.objects.get(phone=phone)

            time_difference = timezone.now() - user.updated_at

            if user.otp == otp:
                if time_difference.total_seconds() <= 300:
                    token = generate_jwt(phone=phone)
                    return JsonResponse({'success': True, 'token': token})
                else:
                    return JsonResponse({'success': False, 'error': 'OTP expired'})
            else:
                return JsonResponse({'success': False, 'error': 'Invalid OTP'})
        except AppUser.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})