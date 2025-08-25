
import flet as ft
import threading
import requests
import json
import ast
import re

# ====== دوال جلب البيانات ======
def get_user_info_new_api(username: str) -> dict | None:
    """
    استخدام الـ API الجديد المحسن لجلب معلومات المستخدم
    """
    try:
        # الخطوة الأولى: البحث عن المستخدم
        search_url = "https://ttpub.linuxtech.io:5004/api/search"
        search_headers = {
            'Host': "ttpub.linuxtech.io:5004",
            'User-Agent': "Dart/3.5 (dart:io)",
            'Accept-Encoding': "gzip",
            'Content-Type': "application/json"
        }
        search_data = {"username": username}
        
        search_res = requests.post(search_url, data=json.dumps(search_data), headers=search_headers, timeout=15)
        search_result = search_res.json()
        
        if 'user' not in search_result or 'sid' not in search_result['user']:
            return None
            
        sid = search_result['user']['sid']
        
        # الخطوة الثانية: جلب تفاصيل المستخدم باستخدام SID
        detail_url = "https://ttpub.linuxtech.io:5004/api/search_by_sid_build_request"
        detail_data = {"sid": sid, "count_requests": 3}
        
        detail_res = requests.post(detail_url, data=json.dumps(detail_data), headers=search_headers, timeout=15)
        detail_result = detail_res.json()
        
        if 'request' not in detail_result or len(detail_result['request']) == 0:
            return None
            
        # الخطوة الثالثة: استخدام URL والـ headers للحصول على البيانات النهائية
        final_url = detail_result['request'][0]["url"]
        final_headers = ast.literal_eval(detail_result['request'][0]["headers"])
        
        final_res = requests.get(final_url, headers=final_headers, timeout=15)
        final_data = final_res.json()
        
        return final_data
        
    except Exception as e:
        print(f"خطأ في جلب البيانات: {e}")
        return None


def format_number(num):
    """تنسيق الأرقام لتكون قابلة للقراءة"""
    if num >= 1000000:
        return f"{num/1000000:.1f}M"
    elif num >= 1000:
        return f"{num/1000:.1f}K"
    else:
        return str(num)


# ====== واجهة Flet ======
def app_main(page: ft.Page):
    page.title = "ELBAD_OFF"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#000000"
    page.window.width = 400
    page.window.height = 700
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = "adaptive"

    # ==== الصفحة الأولى (المقدمة) ====
    splash_image = ft.Image(
        src="https://i.postimg.cc/hPH3KXrp/IMG-20250825-000216-706.jpg",
        width=380, height=300, fit=ft.ImageFit.CONTAIN, border_radius=10
    )
    dev_info = ft.Text(
        "𝐓𝐢𝐤𝐭𝐨𝐤      ► elbad_off\n𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦 ► elbad_off",
        size=16, weight=ft.FontWeight.BOLD, color="#FFFFFF", text_align=ft.TextAlign.CENTER
    )
    btn_contact = ft.ElevatedButton(
        "مراسلة المبرمج", on_click=lambda e: page.launch_url("https://t.me/elbad_off"),
        width=300, height=50,
        style=ft.ButtonStyle(bgcolor="#303F9F", color="#FFFFFF",
                             shape=ft.RoundedRectangleBorder(radius=10))
    )
    def go_next(_):
        build_main_ui()
    btn_skip = ft.ElevatedButton(
        "تخطي", on_click=go_next, width=300, height=50,
        style=ft.ButtonStyle(bgcolor="#D32F2F", color="#FFFFFF",
                             shape=ft.RoundedRectangleBorder(radius=10))
    )
    page.add(
        ft.Container(
            content=ft.Column([ft.Container(height=30), splash_image, ft.Container(height=20),
                               dev_info, ft.Container(height=30), btn_contact,
                               ft.Container(height=15), btn_skip, ft.Container(height=30)],
                              alignment="center", horizontal_alignment="center", spacing=10),
            padding=20, expand=True
        )
    )

    # ==== الواجهة الأساسية ====
    def build_main_ui():
        page.controls.clear()

        top_image = ft.Image(
            src="https://i.postimg.cc/2SBvfwjX/image.jpg",
            width=220, height=220, fit=ft.ImageFit.CONTAIN
        )
        
        # نص ELBAD المتحرك بألوان مختلفة
        animated_text = ft.Text(
            "ELBAD",
            size=40,
            weight=ft.FontWeight.BOLD,
            color="#FF6B6B",
            text_align=ft.TextAlign.CENTER,
            animate_opacity=ft.animation.Animation(1000, ft.AnimationCurve.EASE_IN_OUT),
            animate_color=ft.animation.Animation(1000, ft.AnimationCurve.EASE_IN_OUT)
        )
        
        # دالة تغيير اللون والتأثير
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FECA57", "#FF9FF3", "#54A0FF"]
        color_index = [0]  # استخدام قائمة لتمرير المرجع
        
        def animate_text():
            import time
            while True:
                # تغيير اللون
                animated_text.color = colors[color_index[0] % len(colors)]
                color_index[0] += 1
                
                # تأثير الاختفاء والظهور
                animated_text.opacity = 0.3
                page.update()
                time.sleep(0.5)
                
                animated_text.opacity = 1.0
                page.update()
                time.sleep(0.5)
        
        # بدء التحريك في خيط منفصل
        threading.Thread(target=animate_text, daemon=True).start()
        
        # تحسين مربع إدخال اليوزر
        username_tf = ft.TextField(
            hint_text="ادخل اليوزر",
            width=320,
            height=50,
            text_align=ft.TextAlign.CENTER,
            border_color="#4CAF50",
            focused_border_color="#66BB6A",
            bgcolor="#1A1A1A",
            color="#FFFFFF",
            hint_style=ft.TextStyle(color="#888888"),
            text_style=ft.TextStyle(color="#FFFFFF", size=16),
            border_radius=10,
            content_padding=ft.padding.symmetric(horizontal=15, vertical=10)
        )

        # صندوق النتيجة
        result_text = ft.Text("", color="#FFFFFF", size=12, selectable=True)
        result_box = ft.Container(
            content=ft.Column([result_text], scroll="adaptive"),
            width=350, 
            height=300,
            bgcolor="#111111", 
            border_radius=10, 
            padding=15,
            border=ft.border.all(1, "#333333")
        )

        def fetch_data():
            user = (username_tf.value or "").strip().replace("@", "")
            if not user:
                result_text.value = "⚠️ الرجاء إدخال اليوزر"
                page.update()
                return

            result_text.value = "⏳ جاري جلب البيانات من الـ API الجديد..."
            page.update()

            # جلب البيانات باستخدام الـ API الجديد
            user_data = get_user_info_new_api(user)
            if not user_data:
                result_text.value = "❌ فشل في جلب بيانات المستخدم أو المستخدم غير موجود"
                page.update()
                return

            try:
                # استخراج البيانات من الهيكل الصحيح
                if 'user' not in user_data:
                    result_text.value = "❌ خطأ: لا يمكن العثور على بيانات المستخدم"
                    page.update()
                    return
                
                user_info = user_data['user']
                
                # المعلومات الأساسية
                uid = user_info.get('uid', 'غير متوفر')
                username = user_info.get('unique_id', 'غير متوفر')
                nickname = user_info.get('nickname', 'غير متوفر')
                signature = user_info.get('signature', 'لا يوجد')
                sec_uid = user_info.get('sec_uid', 'غير متوفر')
                
                # الإحصائيات
                followers = user_info.get('follower_count', 0)
                following = user_info.get('following_count', 0)
                total_favorited = user_info.get('total_favorited', 0)
                videos = user_info.get('aweme_count', 0)
                favoriting_count = user_info.get('favoriting_count', 0)
                
                # معلومات التحقق والخصوصية
                verification_type = user_info.get('verification_type', 0)
                verified = verification_type > 0
                custom_verify = user_info.get('custom_verify', '')
                
                # معلومات إضافية
                avatar_medium = user_info.get('avatar_medium', {})
                avatar_url = ''
                if avatar_medium and 'url_list' in avatar_medium and avatar_medium['url_list']:
                    avatar_url = avatar_medium['url_list'][0]
                
                # معلومات الحساب
                account_type = user_info.get('account_type', 0)
                is_star = user_info.get('is_star', False)
                is_effect_artist = user_info.get('is_effect_artist', False)
                live_commerce = user_info.get('live_commerce', False)
                
                # معلومات المشاركة
                share_info = user_info.get('share_info', {})
                share_url = share_info.get('share_url', f'https://www.tiktok.com/@{username}')
                
                # معلومات التجارة
                commerce_user_level = user_info.get('commerce_user_level', 0)
                with_commerce_entry = user_info.get('with_commerce_entry', False)
                
                # معلومات الموسيقى
                original_musician = user_info.get('original_musician', {})
                music_count = original_musician.get('music_count', 0)
                music_used_count = original_musician.get('music_used_count', 0)
                
                # معدلات المشاركة
                mplatform_followers = user_info.get('mplatform_followers_count', 0)
                
                # نوع الحساب
                account_type_text = {
                    0: 'عادي',
                    1: 'تجاري', 
                    2: 'منشئ محتوى',
                    3: 'مؤسسة'
                }.get(account_type, 'غير معروف')
                
                # تنسيق النتيجة مع جميع المعلومات المتوفرة
                result_text.value = (
                    "╔══════════════════════════════╗\n"
                    "║           𝚃𝙸𝙺𝚃𝙾𝙺 𝙸𝙽𝙵𝙾           ║\n"
                    "╠══════════════════════════════╣\n"
                    f"║ 𝐍𝐀𝐌𝐄 ➤ {nickname}\n"
                    f"║ 𝐔𝐒𝐄𝐑𝐍𝐀𝐌𝐄 ➤ @{username}\n"
                    f"║ 𝐔𝐈𝐃 ➤ {uid}\n"
                    f"║ 𝐒𝐄𝐂_𝐔𝐈𝐃 ➤ {sec_uid[:25]}...\n"
                    "╠══════════════════════════════╣\n"
                    f"║ 𝐅𝐎𝐋𝐋𝐎𝐖𝐄𝐑𝐒 ➤ {format_number(followers)}\n"
                    f"║ 𝐅𝐎𝐋𝐋𝐎𝐖𝐈𝐍𝐆 ➤ {format_number(following)}\n"
                    f"║ 𝐓𝐎𝐓𝐀𝐋 𝐋𝐈𝐊𝐄𝐒 ➤ {format_number(total_favorited)}\n"
                    f"║ 𝐕𝐈𝐃𝐄𝐎𝐒 ➤ {format_number(videos)}\n"
                    f"║ 𝐅𝐀𝐕𝐎𝐑𝐈𝐓𝐄𝐒 ➤ {format_number(favoriting_count)}\n"
                    "╠══════════════════════════════╣\n"
                    f"║ 𝐕𝐄𝐑𝐈𝐅𝐈𝐄𝐃 ➤ {'✅ نعم' if verified else '❌ لا'}\n"
                    f"║ 𝐀𝐂𝐂𝐎𝐔𝐍𝐓 𝐓𝐘𝐏𝐄 ➤ {account_type_text}\n"
                    f"║ 𝐒𝐓𝐀𝐑 ➤ {'⭐ نعم' if is_star else '❌ لا'}\n"
                    f"║ 𝐄𝐅𝐅𝐄𝐂𝐓 𝐀𝐑𝐓𝐈𝐒𝐓 ➤ {'🎨 نعم' if is_effect_artist else '❌ لا'}\n"
                    "╠══════════════════════════════╣\n"
                    f"║ 𝐌𝐔𝐒𝐈𝐂 𝐂𝐎𝐔𝐍𝐓 ➤ {format_number(music_count)}\n"
                    f"║ 𝐌𝐔𝐒𝐈𝐂 𝐔𝐒𝐄𝐃 ➤ {format_number(music_used_count)}\n"
                    f"║ 𝐂𝐎𝐌𝐌𝐄𝐑𝐂𝐄 ➤ {'💼 نعم' if with_commerce_entry else '❌ لا'}\n"
                    f"║ 𝐋𝐈𝐕𝐄 𝐂𝐎𝐌𝐌𝐄𝐑𝐂𝐄 ➤ {'🔴 نعم' if live_commerce else '❌ لا'}\n"
                    "╠══════════════════════════════╣\n"
                    f"║ 𝐁𝐈𝐎 ➤ {signature[:30] if signature else 'لا يوجد'}{'...' if len(signature) > 30 else ''}\n"
                    f"║ 𝐕𝐄𝐑𝐈𝐅𝐘 ➤ {custom_verify if custom_verify else 'لا يوجد'}\n"
                    f"║ 𝐔𝐑𝐋 ➤ tiktok.com/@{username}\n"
                    "╚══════════════════════════════╝\n"
                    f"\n🔗 𝐀𝐕𝐀𝐓𝐀𝐑: {avatar_url[:50] if avatar_url else 'غير متوفر'}{'...' if len(avatar_url) > 50 else ''}\n"
                    "\n═══════════ 𝙱𝚈 @𝙴𝙻𝙱𝙰𝙳_𝙾𝙵𝙵 ═══════════"
                )
                
                # تحديث الواجهة بعد نجاح معالجة البيانات
                page.update()
                    
            except Exception as e:
                result_text.value = (
                    f"❌ خطأ في تحليل البيانات: {str(e)}\n\n"
                    "البيانات المستلمة:\n" + 
                    (str(user_data)[:500] + "..." if len(str(user_data)) > 500 else str(user_data))
                )
                page.update()

        def on_start_click(_):
            threading.Thread(target=fetch_data, daemon=True).start()

        start_btn = ft.ElevatedButton(
            "🔍 البحث", on_click=on_start_click, width=220, height=48,
            style=ft.ButtonStyle(
                bgcolor="#4CAF50", 
                color="#FFFFFF",
                shape=ft.RoundedRectangleBorder(radius=10),
                elevation=3
            )
        )

        page.add(
            ft.Column(
                [top_image, animated_text, ft.Container(height=10), username_tf, ft.Container(height=8),
                 start_btn, ft.Container(height=14), result_box],
                alignment="center", horizontal_alignment="center", spacing=10
            )
        )
        page.update()

# تشغيل التطبيق
if __name__ == "__main__":
    # للتطوير - تشغيل كتطبيق ويب
    ft.app(target=app_main, view=ft.AppView.WEB_BROWSER, port=5000, host="0.0.0.0")
