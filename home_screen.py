
import flet as ft
import numpy as np
import pandas as pd
import pickle
import os
import platform
from datetime import datetime
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_RIGHT
from fuzzywuzzy import process
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import flet as ft
import google.generativeai as genai
import google.ai.generativelanguage as glm
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import flet as ft
import pathlib
import google.generativeai as genai
import google.ai.generativelanguage as glm
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
from datetime import datetime





sym_des = pd.read_csv("symtoms_df.csv")
precautions = pd.read_csv("p.csv")
workout = pd.read_csv("w.csv")
description = pd.read_csv("des.csv")
medications = pd.read_csv('med.csv')
diets = pd.read_csv("d.csv")
test_lap = pd.read_csv("test_lap.csv") 
svc = pickle.load(open('svc.pkl', 'rb'))

def helper(dis):
    desc = description[description['Disease'] == dis]['Description'].iloc[0]
    pre = [str(p) for p in precautions[precautions['Disease'] == dis][
        ['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']].values.tolist()[0]]
    med = [str(m) for m in medications[medications['Disease'] == dis]['Medication'].values.tolist()]
    die = [str(d) for d in diets[diets['Disease'] == dis]['Diet'].values.tolist()]
    wrkout = [str(w) for w in workout[workout['disease'] == dis]['workout'].values.tolist()]
    # إضافة استرجاع الفحوصات
    tests = test_lap[test_lap['Disease'] == dis]['test_lap'].iloc[0] if not test_lap[test_lap['Disease'] == dis].empty else "لا توجد فحوصات محددة"

    return desc, pre, med, die, wrkout, tests 
# تقيؤ رجفة حمى مرتفعة تعرق صداع غثيان إسهال ألم في العضلات  مرض الملاريا
# طفح جلدي رجفة ألم المفاصل تقيؤ تعب حمى مرتفعة صداع غثيان حمئ الضنك 
# مرض الربؤ تعب سعالحمى مرتفعة ضيق التنفس
# مرض قرحة المعدة تقيؤ عسر الهضمفقدان الشهية ألم في البطن انتفاخ البطن حكة داخلية
# مرض جلطة دماغية او الشلل  تقيؤ صداع ضعف في جانب واحد من الجسم تغير في الوعي

symptoms_dict = {

    'itching': 0, 'حكة': 0,
    'skin_rash': 1, 'طفح جلدي': 1,
    'nodal_skin_eruptions': 2, 'نتوءات جلدية عقدية': 2,
    'continuous_sneezing': 3, 'عطس مستمر': 3,
    'shivering': 4, 'قشعريرة': 4,
    'chills': 5, 'رجفة': 5, 
    'joint_pain': 6, 'ألم المفاصل': 6,
    'stomach_pain': 7, 'ألم في المعدة': 7,
    'acidity': 8, 'حموضة': 8,
    'ulcers_on_tongue': 9, 'تقرحات على اللسان': 9,
    'muscle_wasting': 10, 'ضمور العضلات': 10,
    'vomiting': 11, 'تقيؤ  طرش': 11,
    'burning_micturition': 12, 'حرقة أثناء التبول': 12,
    'spotting_ urination': 13, 'تبول متقطع': 13,
    'fatigue': 14, 'تعب': 14,
    'weight_gain': 15, 'زيادة الوزن': 15,
    'anxiety': 16, 'قلق': 16,
    'cold_hands_and_feets': 17, 'برودة اليدين والقدمين': 17,
    'mood_swings': 18, 'تقلبات المزاج': 18,
    'weight_loss': 19, 'فقدان الوزن': 19,
    'restlessness': 20, 'تململ': 20,
    'lethargy': 21, 'خمول': 21,
    'patches_in_throat': 22, 'بقع في الحلق': 22,
    'irregular_sugar_level': 23, 'مستوى سكر غير منتظم': 23,
    'cough': 24, ' سعلة سعال': 24,
    'high_fever': 25, 'حمى مرتفعة': 25,
    'sunken_eyes': 26, 'عيون غائرة': 26,
    'breathlessness': 27, 'ضيق التنفس': 27,
    'sweating': 28, 'تعرق': 28,
    'dehydration': 29, 'جفاف': 29,
    'indigestion': 30, 'عسر الهضم': 30,
    'headache': 31, ' زكام صداع': 31,
    'yellowish_skin': 32, 'جلد مصفر': 32,
    'dark_urine': 33, 'بول داكن': 33,
    'nausea': 34, 'غثيان': 34,
    'loss_of_appetite': 35, 'فقدان الشهية': 35,
    'pain_behind_the_eyes': 36, 'ألم خلف العينين': 36,
    'back_pain': 37, 'ألم الظهر': 37,
    'constipation': 38, 'إمساك': 38,
    'abdominal_pain': 39, 'ألم في البطن': 39,
    'diarrhoea': 40, 'إسهال': 40,
    'mild_fever': 41, 'حمى خفيفة': 41,
    'yellow_urine': 42, 'بول أصفر': 42,
    'yellowing_of_eyes': 43, 'اصفرار العينين': 43,
    'acute_liver_failure': 44, 'فشل كبدي حاد': 44,
    'fluid_overload': 45, 'زيادة السوائل': 45,
    'swelling_of_stomach': 46, 'انتفاخ المعدة': 46,
    'swelled_lymph_nodes': 47, 'تورم الغدد الليمفاوية': 47,
    'malaise': 48, 'توعك': 48,
    'blurred_and_distorted_vision': 49, 'رؤية مشوشة ومشوهة': 49,
    'phlegm': 50, 'بلغم': 50,
    'throat_irritation': 51, 'تهيج الحلق': 51,
    'redness_of_eyes': 52, 'احمرار العينين': 52,
    'sinus_pressure': 53, 'ضغط الجيوب الأنفية': 53,
    'runny_nose': 54, 'سيلان الأنف': 54,
    'congestion': 55, 'احتقان': 55,
    'chest_pain': 56, 'ألم في الصدر': 56,
    'weakness_in_limbs': 57, 'ضعف في الأطراف': 57,
    'fast_heart_rate': 58, 'سرعة ضربات القلب': 58,
    'pain_during_bowel_movements': 59, 'ألم أثناء التبرز': 59,
    'pain_in_anal_region': 60, 'ألم في منطقة الشرج': 60,
    'bloody_stool': 61, 'براز دموي': 61,
    'irritation_in_anus': 62, 'تهيج في الشرج': 62,
    'neck_pain': 63, 'ألم الرقبة': 63,
    'dizziness': 64, 'دوخة': 64,
    'cramps': 65, 'تقلصات': 65,
    'bruising': 66, 'كدمات': 66,
    'obesity': 67, 'سمنة': 67,
    'swollen_legs': 68, 'ساقين متورمتين': 68,
    'swollen_blood_vessels': 69, 'أوعية دموية منتفخة': 69,
    'puffy_face_and_eyes': 70, 'وجه وعيون منتفخة': 70,
    'enlarged_thyroid': 71, 'تضخم الغدة الدرقية': 71,
    'brittle_nails': 72, 'أظافر هشة': 72,
    'swollen_extremeties': 73, 'أطراف متورمة': 73,
    'excessive_hunger': 74, 'جوع مفرط': 74,
    'extra_marital_contacts': 75, 'علاقات خارج الزواج': 75,
    'drying_and_tingling_lips': 76, 'جفاف ووخز الشفاه': 76,
    'slurred_speech': 77, 'تأتأة': 77,
    'knee_pain': 78, 'ألم الركبة': 78,
    'hip_joint_pain': 79, 'ألم مفصل الورك': 79,
    'muscle_weakness': 80, 'ضعف العضلات': 80,
    'stiff_neck': 81, 'تصلب الرقبة': 81,
    'swelling_joints': 82, 'تورم المفاصل': 82,
    'movement_stiffness': 83, 'تصلب الحركة': 83,
    'spinning_movements': 84, 'حركات دورانية': 84,
    'loss_of_balance': 85, 'فقدان التوازن': 85,
    'unsteadiness': 86, 'تذبذب': 86,
    'weakness_of_one_body_side': 87, 'ضعف في جانب واحد من الجسم': 87,
    'loss_of_smell': 88, 'فقدان الشم': 88,
    'bladder_discomfort': 89, 'انزعاج المثانة': 89,
    'foul_smell_of urine': 90, 'رائحة بول كريهة': 90,
    'continuous_feel_of_urine': 91, 'الشعور المستمر بالتبول': 91,
    'passage_of_gases': 92, 'انتفاخ البطن': 92,
    'internal_itching': 93, 'حكة داخلية': 93,
    'toxic_look_(typhos)': 94, 'مظهر سام (تيفوس)': 94,
    'depression': 95, 'اكتئاب': 95,
    'irritability': 96, 'تهيج': 96,
    'muscle_pain': 97, 'ألم في العضلات': 97,
    'altered_sensorium': 98, 'تغير في الوعي': 98,
    'red_spots_over_body': 99, 'بقع حمراء على الجسم': 99,
    'belly_pain': 100, 'ألم في البطن': 100,
    'abnormal_menstruation': 101, 'دورة شهرية غير طبيعية': 101,
    'dischromic_patches': 102, 'بقع متغيرة اللون': 102,
    'watering_from_eyes': 103, 'دموع من العين': 103,
    'increased_appetite': 104, 'زيادة الشهية': 104,
    'polyuria': 105, 'تبول مفرط': 105,
    'family_history': 106, 'تاريخ عائلي': 106,
    'mucoid_sputum': 107, 'بلغم مخاطي': 107,
    'rusty_sputum': 108, 'بلغم صدئ': 108,
    'lack_of_concentration': 109, 'قلة التركيز': 109,
    'visual_disturbances': 110, 'اضطرابات بصرية': 110,
    'receiving_blood_transfusion': 111, 'تلقي نقل دم': 111,
    'receiving_unsterile_injections': 112, 'تلقي حقن غير معقمة': 112,
    'coma': 113, 'غيبوبة': 113,
    'stomach_bleeding': 114, 'نزيف في المعدة': 114,
    'distention_of_abdomen': 115, 'انتفاخ البطن': 115,
    'history_of_alcohol_consumption': 116, 'تاريخ تعاطي الكحول': 116,
    'fluid_overload.1': 117, # قد تحتاج إلى معالجة هذه التسمية المكررة
    'blood_in_sputum': 118, 'دم في البلغم': 118,
    'prominent_veins_on_calf': 119, 'أوردة بارزة في ربلة الساق': 119,
    'palpitations': 120, 'خفقان': 120,
    'painful_walking': 121, 'مشي مؤلم': 121,
    'pus_filled_pimples': 122, 'بثور مليئة بالصديد': 122,
    'blackheads': 123, 'رؤوس سوداء': 123,
    'scurring': 124, 'تقشر': 124,
    'skin_peeling': 125, 'تقشير الجلد': 125,
    'silver_like_dusting': 126, 'غبار فضي': 126,
    'small_dents_in_nails': 127, 'نقر صغير في الأظافر': 127,
    'inflammatory_nails': 128, 'التهاب الأظافر': 128,
    'blister': 129, 'بثور': 129,
    'red_sore_around_nose': 130, 'تقرحات حمراء حول الأنف': 130,
    'yellow_crust_ooze': 131, 'إفرازات صفراء متقشرة': 131,
    'حرقان أثناء التبول': 12, # إضافة النسخة العربية
    'تبول متقطع': 13, # إضافة النسخة العربية
    'الم في المعدة': 7 # إضافة النسخة العربية
}

diseases_list = {
    15: 'عدوى فطرية',
    4: 'حساسية',
    16: 'ارتجاع المريء',
    9: 'ركود الصفراء المزمن',
    14: 'تفاعل دوائي',
    33: 'قرحة المعدة',
    1: 'الإيدز',
    12: 'السكري',
    17: 'التهاب المعدة والأمعاء',
    6: 'الربو الشعبي',
    23: 'ارتفاع ضغط الدم',
    30: 'الصداع النصفي',
    7: 'تآكل الفقرات العنقية',
    32: '  جلطة  (نزيف المخ)',
    28: 'اليرقان',
    29: 'الملاريا',
    8: 'جدري الماء',
    11: 'حمى الضنك',
    37: 'التيفوئيد',
    40: 'التهاب الكبد أ',
    19: 'التهاب الكبد ب',
    20: 'التهاب الكبد ج',
    21: 'التهاب الكبد د',
    22: 'التهاب الكبد ه',
    3: 'التهاب الكبد الكحولي',
    36: 'السل',
    10: 'نزلة البرد',
    34: 'الالتهاب الرئوي',
    13: 'البواسير',
    18: 'النوبة القلبية',
    39: 'الدوالي',
    26: 'قصور الغدة الدرقية',
    24: 'فرط نشاط الغدة الدرقية',
    25: 'نقص سكر الدم',
    31: 'التهاب المفاصل العظمي',
    5: 'التهاب المفاصل',
    0: 'الدوار الوضعي',
    2: 'حب الشباب',
    38: 'التهاب المسالك البولية',
    35: 'الصدفية',
    27: 'القوباء'
}


def get_predicted_value(patient_symptoms):
    try:
        num_unique_symptoms = len(set(symptoms_dict.values()))
        input_vector = np.zeros(num_unique_symptoms)

        for item in patient_symptoms:
            item = item.strip()

            for key, value in symptoms_dict.items():
                if item == key:
                    input_vector[value] = 1
                    break 


        input_vector = input_vector.astype(float)
        prediction = svc.predict([input_vector])[0]
        return diseases_list[prediction]
    except Exception as e:
        raise Exception(f"Prediction failed: {str(e)}")


def suggest_symptoms(user_input):
    english_choices = [key for key in symptoms_dict if isinstance(key, str) and key.isascii()]
    arabic_choices = [key for key in symptoms_dict if isinstance(key, str) and not key.isascii()]

    english_suggestions = process.extract(user_input, english_choices, limit=5)
    arabic_suggestions = process.extract(user_input, arabic_choices, limit=5)

    suggestions = [symptom for symptom, score in english_suggestions] + [symptom for symptom, score in
                                                                         arabic_suggestions]
    return list(set(suggestions))



class Splash(ft.View):
    def __init__(self):
        super().__init__()
        self.route = "/" 
        self.padding = ft.padding.all(0) 
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.bgcolor = "#E6F3F3"  

     
        self.header = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text(
                        "تطبيق التشخيص الطبي",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.WHITE,  
                        font_family="Cairo",
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER, 
            ),
            bgcolor="#87CEEB", 
            padding=ft.padding.symmetric(vertical=10), 
            height=70, 
    
            alignment=ft.alignment.center,
        )

        # --- Texts ---
        self.app_title = ft.Text(
            value="اكتشف صحتك بسهولة",
            size=28,  # حجم أكبر قليلاً
            weight=ft.FontWeight.BOLD,
            color="#004AAD",  # نفس اللون الأزرق الداكن
            font_family="Cairo",
            text_align=ft.TextAlign.CENTER,
        )

        self.welcome_message = ft.Text(
            value="ابدأ رحلة التشخيص الذكي الآن", 
            size=16,
            color=ft.colors.GREY_700, 
            text_align=ft.TextAlign.CENTER,
            font_family="Cairo"
        )

        # --- Buttons ---
        def create_styled_button(text, route):
            return ft.ElevatedButton(
                content=ft.Text(
                    value=text,
                    color=ft.colors.WHITE,
                    font_family="Cairo",
                    size=16,
                    weight=ft.FontWeight.W_500,
                ),
                width=280, 
                height=55,  
                style=ft.ButtonStyle(
                    bgcolor={
                        ft.MaterialState.DEFAULT: "#87CEEB", 
                        ft.MaterialState.HOVERED: "#0056b3",  
                    },
                    shape=ft.RoundedRectangleBorder(radius=12), 
                    elevation={
                        ft.MaterialState.DEFAULT: 2,
                        ft.MaterialState.HOVERED: 4
                    }
                ),
                on_click=lambda e: e.page.go(route)
            )

        self.btn1 = create_styled_button("كتابة الأعراض", "/home")
        self.btn_pain = create_styled_button("تحديد الأعراض", "/home2") # نص أوضح
        self.btn2 = create_styled_button("تحليل صورة الفحص", "/MedicalAnalysisApp")


        # --- Card ---
        self.button_card = ft.Card(
            elevation=4,  # ظل أقل
            color="#FFFFFF",  
            content=ft.Container(
                content=ft.Column(
                    [
                        self.btn_pain,
                        ft.Divider(height=5, color="transparent"), # فاصل
                        self.btn1,
                        ft.Divider(height=5, color="transparent"),
                        self.btn2,
                    ],
                    spacing=10,  
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                width=300,
                padding=ft.padding.all(30),
                border_radius=ft.border_radius.all(20)
            )
        )

        # --- Main Content ---
        self.splash_content = ft.Container(
            content=ft.Column(
                [
                
                    ft.Divider(height=20, color="transparent"), # فاصل
                    self.welcome_message,
                    ft.Divider(height=40, color="transparent"), # فاصل أكبر
                    self.button_card,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
  
            expand=True, 
        )

        self.controls = [self.header, self.splash_content] 

PRIMARY_COLOR = "#87CEEB"  # Sky Blue
SECONDARY_COLOR = "#4682B4"  # Steel Blue
ERROR_COLOR = "#DB4437"
TEXT_COLOR = "#333333" 
BG_COLOR = "#F0F4F8"  
BUTTON_HOVER_COLOR = "#60A5D8" 

class WelcomeScreen(ft.View):
    def __init__(self, results_data):
        super().__init__(
            padding=0,
            bgcolor="white" 
        )
        self.results_data = results_data
        self.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    
        self.__title = ft.Text(
            value="تطبيق التشخيص الطبي", 
            color=ft.colors.BLUE_GREY_900,  
            size=28,  
            font_family="Cairo",  
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        )

        self.__logo = self._create_logo() 
        self.__user_greeting = self._create_user_greeting()

        # Main container, mimicking SplashFirst's structure
        self.__container = ft.Container(
            width=380,
            height=750,
            content=ft.Column(
                controls=[
                    self.__title,
                    self.__logo,
                    ft.Container(height=20),  # Spacing
                    self.__user_greeting,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            gradient=ft.LinearGradient(  # Same gradient as SplashFirst
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=["#87CEEB", "#D3D3D3"]
            ),
            border=ft.border.all(1, ft.colors.GREY_300), # subtle border
        )

        self.controls = [self.__container]



    def _create_logo(self):
        return ft.Container(
            content=ft.Image(
                src="ai.jpg",
                width=180, 
                height=180,
                fit=ft.ImageFit.CONTAIN,  
                border_radius=ft.border_radius.all(90),  # Circular
            ),
            margin=ft.margin.only(top=10, bottom=10),  # Adjust margins
            alignment=ft.alignment.center,
             shadow=ft.BoxShadow( 
                spread_radius=1,
                blur_radius=8,
                color=ft.colors.GREY_400,
                offset=ft.Offset(0, 4),
            ),
        )

    def _create_user_greeting(self):
        return ft.Container(
            content=ft.Text(
                value=f"مرحبًا بك يا {self.results_data.get('patient_name', 'مستخدم')}!",
                color=ft.colors.BLUE_GREY_800, 
                size=22,
                font_family="Cairo",
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
            ),
            padding=ft.padding.only(top=5, bottom=5),
        )


class PatientInfo(ft.View):
    def __init__(self):
        super().__init__(
            route="/PatientInfo",
            padding=ft.padding.all(20),
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            bgcolor=BG_COLOR,
        )

        self.page_title = self._create_page_title()
        self.patient_name = self._create_text_field("اسم المريض", "أدخل اسم المريض هنا")
        self.patient_age = self._create_text_field(
            "العمر", "أدخل العمر هنا", ft.KeyboardType.NUMBER
        )
        self.patient_gender = self._create_dropdown("الجنس", ["ذكر", "أنثى"])
        self.submit_button = self._create_elevated_button("إرسال", self.predict_disease)
        self.input_card = self._create_input_card()
        self.controls = [self.input_card]

    def _create_rounded_container(self, content, width=None, height=None, bgcolor=None, border_radius=15, padding=10, alignment=ft.alignment.center):
      """Creates a container with rounded corners (within the class)."""
      return ft.Container(
          content=content,
          width=width,
          height=height,
          bgcolor=bgcolor,
          border_radius=ft.border_radius.all(border_radius),
          padding=padding,
          alignment=alignment
      )

    def _create_page_title(self):
        return ft.Text(
            value="معلومات المريض",
            size=30,
            weight=ft.FontWeight.BOLD,
            color=SECONDARY_COLOR,
        )

    def _create_text_field(self, label: str, hint: str, keyboard_type: ft.KeyboardType = None, width=300, height=55) -> ft.TextField:
        return ft.TextField(
            label=label,
            hint_text=hint,
            border_color=SECONDARY_COLOR,
            width=width,
            height=height,
            border_radius=ft.border_radius.all(10),
            keyboard_type=keyboard_type,
        )

    def _create_dropdown(self, label: str, options: list[str], width=300, height=55) -> ft.Dropdown:
        return ft.Dropdown(
            options=[ft.dropdown.Option(option) for option in options],
            label=label,
            width=width,
            height=height,
            border_color=SECONDARY_COLOR,
            border_radius=ft.border_radius.all(10),
        )

    def _create_elevated_button(self, text: str, on_click_handler, width=250, height=50) -> ft.ElevatedButton:
        return ft.ElevatedButton(
            content=ft.Text(
                value=text,
                color=ft.colors.WHITE,
                size=18,
                weight=ft.FontWeight.W_500,
            ),
            width=width,
            height=height,
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.DEFAULT: SECONDARY_COLOR,
                    ft.ControlState.HOVERED: BUTTON_HOVER_COLOR,
                },
                shape=ft.RoundedRectangleBorder(radius=10),
                elevation={
                    ft.ControlState.DEFAULT: 3,
                    ft.ControlState.HOVERED: 6,
                },
            ),
            on_click=on_click_handler,
        )

    def _create_input_card(self):
      return ft.Card(
          elevation=8,
          color=ft.colors.WHITE,
          surface_tint_color=ft.colors.WHITE,
          content=self._create_rounded_container(
              content=ft.Column(
                  [
                      self.page_title,
                      self.patient_name,
                      self.patient_age,
                      self.patient_gender,
                      ft.Container(height=20),
                      self.submit_button,
                  ],
                  spacing=18,
                  alignment=ft.MainAxisAlignment.CENTER,
                  horizontal_alignment=ft.CrossAxisAlignment.CENTER,
              ),
              width=350,
              padding=ft.padding.all(25),
              bgcolor=ft.colors.WHITE,
              border_radius=20,
          ),
      )

    def _show_error_dialog(self, message: str):
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("خطأ", color=ERROR_COLOR),
            content=ft.Text(message),
            actions=[ft.TextButton("موافق", on_click=lambda e: self._close_dlg(dlg))],
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def _close_dlg(self, dlg: ft.AlertDialog):
        dlg.open = False
        self.page.update()

    def validate_input(self):
        if not self.patient_name.value:
            return "يرجى إدخال اسم المريض."
        if not self.patient_age.value:
            return "يرجى إدخال العمر."
        try:
            age = int(self.patient_age.value)
            if age <= 0:
                return "العمر يجب أن يكون أكبر من صفر."
        except ValueError:
            return "يرجى إدخال رقم صحيح للعمر."
        if not self.patient_gender.value:
            return "يرجى اختيار الجنس."
        return None

    def predict_disease(self, e):
        error = self.validate_input()
        if error:
            self._show_error_dialog(error)
            return

        self.page.results_data = {
            "patient_name": self.patient_name.value,
            "gender": self.patient_gender.value,
            "age": self.patient_age.value,
        }

        self.page.update()
        self.page.go("/WelcomeScreen")

class SplashFirst(ft.View):
    def __init__(self):
        super().__init__(
            padding=0,
            bgcolor="white"  # تم تغيير لون الخلفية الافتراضي
        )
        
        # إنشاء العنوان
        self.__title = ft.Text(
            value="AI Health Check",
            color=ft.colors.BLACK,  # تغيير لون النص إلى الأسود ليظهر بشكل أفضل
            size=30,
            font_family="Poppins",
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER
        )

        # إنشاء حاوية للشعار
        self.__logo = ft.Container(
            content=ft.Image(
                src="ai.jpg",
                width=200,
                height=200,
                fit=ft.ImageFit.CONTAIN,
            ),
            margin=ft.margin.only(top=20, bottom=20),
            alignment=ft.alignment.center
        )
        self.__container = ft.Container(
            width=380,
            height=750,
            content=ft.Column(
                controls=[
                    self.__title,
                    self.__logo
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[
                    "#87CEEB",  # لون سماوي
                    "#D3D3D3"   # لون رمادي
                ]
            )
        )

        # إعداد موقع النافذة
        self.window_left = 898
        self.window_top = 0.5
        
        self.controls = [self.__container]

    async def did_mount_async(self):
        self.page.window_width = 380
        self.page.window_height = 750
        self.page.window_left = 898
        self.page.window_top = 0.5
        self.page.padding = 0
        self.page.update()




class MedicalAnalysisApp(ft.View):
    def __init__(self):
        super().__init__(
            route="/MedicalAnalysisApp",
            bgcolor="#E6F3F3",  # Consistent background color
            padding=0
        )

        self.image_path = None
        self.detailed_analysis = None

        try:
            genai.configure(api_key='AIzaSyDXdDHo2UfbnEjUVkJHshwbIIPetOZr0IQ') 
            self.model_vision = genai.GenerativeModel('gemini-1.5-flash') 
            self.chat_vision = self.model_vision.start_chat(history=[])
            pdfmetrics.registerFont(TTFont('Arabic', 'Arial.ttf'))  
        except Exception as init_error:
            print(f"Error initializing: {str(init_error)}")
            raise

        self.chat = ft.ListView(
            expand=True,
            spacing=10,  # Reduced spacing
            auto_scroll=True,
            padding=ft.padding.all(15), # Consistent padding
        )

        self.pick_files_dialog = ft.FilePicker(
            on_result=self.pick_files_result
        )

        self.setup_ui()

    def setup_ui(self):
        # --- Header ---
        self.__header = ft.Container(
            content=ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        icon_color="#004AAD",  # Dark blue
                        on_click=lambda e: e.page.go("/")  # Or appropriate back route
                    ),
                    ft.Text(
                        "تحليل الفحوصات",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color="#004AAD",
                        font_family="Cairo", # Consistent font
                    ),
                    # Placeholder to center the title (using expanded container)
                    ft.Container(expand=True)
                ],
                alignment=ft.MainAxisAlignment.START,  # Align to start
            ),
            bgcolor="#87CEEB",  # Light blue
            padding=ft.padding.symmetric(vertical=10),  # Vertical padding only
            height=70,
            alignment=ft.alignment.center, # Center-align content
        )

        # --- Chat container ---
        chat_container = ft.Container(
            content=self.chat,
            border_radius=15,
            padding=0,  # Padding handled by chat itself
            margin=ft.margin.symmetric(horizontal=20),
            expand=True,
            bgcolor="#FFFFFF", # White background for the chat
            # Optional subtle shadow
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=5,
                color=ft.colors.GREY_300,
                offset=ft.Offset(0, 2),
            )
        )

        # --- Buttons ---
        button_style = ft.ButtonStyle(
            color="#FFFFFF",  # White text
            bgcolor={
                ft.MaterialState.DEFAULT: "#007BFF",  # Blue
                ft.MaterialState.HOVERED: "#0056b3",   # Darker blue on hover
            },
            padding=ft.padding.all(12), # Consistent padding
            animation_duration=300,
            shape=ft.RoundedRectangleBorder(radius=10), # Rounded corners
            elevation={ # Shadow
                ft.MaterialState.DEFAULT: 2,
                ft.MaterialState.HOVERED: 4
            }
        )

        buttons = ft.Row(
            [
                ft.ElevatedButton(
                    "رفع صورة الفحص",
                    icon=ft.icons.UPLOAD_FILE,
                    on_click=self.pick_file,
                    style=button_style
                ),
                ft.ElevatedButton(
                    "مسح المحادثة",
                    icon=ft.icons.CLEAR_ALL,
                    on_click=self.clear_chat,
                    style=button_style
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=15,  # Consistent spacing
        )

        button_container = ft.Container(
            content=buttons,
            padding=ft.padding.symmetric(vertical=15),  # Vertical padding only
        )


        # --- Main layout ---
        self.controls = [
            self.pick_files_dialog,  # For file picking
            ft.Column(
                [
                    self.__header,
                    # app_header,  <-- Removed, title is now in header
                    chat_container,
                    button_container,
                ],
                spacing=0,  # Remove spacing between major sections
                expand=True,  # Expand to fill the screen
                # tight=True  <-- Not needed with expand=True
            )
        ]

    async def did_mount_async(self):
        self.page.pubsub.subscribe(self.on_message)
        self.page.bgcolor = "#E6F3F3"
        self.page.window_width = 360
        self.page.window_height = 750
        self.page.window_resizable = False
        self.page.window.top = 0
        self.page.window.left = 898
        self.page.padding = 0
        if self.pick_files_dialog not in self.page.overlay:
             self.page.overlay.append(self.pick_files_dialog)
        await self.page.update_async()

    def pick_files_result(self, e: ft.FilePickerResultEvent):
      if e.files:
        try:
            self.image_path = e.files[0].path
            self.add_message("Me", self.image_path, is_image=True)
            summary = self.analyze_image() # Get the summary
            if summary:
                result_container = self.create_result_container(summary)
                self.add_message("AI", result_container) # Display the summary

        except Exception as error:
             self.add_message("AI", f"خطأ في تحليل الصورة: {str(error)}")
             print(f"Error in pick_files_result: {str(error)}") # For debugging


    def add_message(self, user_name: str, content, is_image: bool = False):
        message = self.create_chat_message(user_name, content, is_image)
        self.chat.controls.append(message)
        self.page.update()

    def create_chat_message(self, user_name: str, content, is_image: bool = False):
        avatar_color = "#87CEEB" if user_name == "Me" else "#007BFF"  # Distinct colors
        avatar = ft.CircleAvatar(
            content=ft.Text(
                user_name[:1].capitalize(),
                size=14,
                weight="bold"
            ),
            color="white",
            bgcolor=avatar_color,
            radius=18,  # Slightly smaller avatar
        )

        message_container = ft.Container(
            bgcolor="#FFFFFF", # White message background
            border_radius=10,  # Rounded corners
            padding=ft.padding.all(10),  # Consistent padding
            # animate=ft.animation.Animation(300, "easeOut"), # Optional animation
        )

        if is_image:
            message_container.content = ft.Column([
                ft.Text(user_name, weight="bold", color="#004AAD"),
                ft.Image(
                    src=content,
                    width=250,  # Larger image display
                    height=250,
                    fit=ft.ImageFit.CONTAIN,
                    border_radius=8, # Rounded image corners
                ),
            ], tight=True, spacing=5)
        else:
            if isinstance(content, ft.Container):
                message_container.content = content  # If it's already a container, use it directly
            else:
                message_container.content = ft.Column([
                    ft.Text(user_name, weight="bold", color="#004AAD"),
                    ft.Text(
                        str(content),
                        selectable=True,
                        size=14,
                        color="black",
                    ),
                ], tight=True, spacing=5)


        return ft.Row(
            [avatar, ft.Container(content=message_container, expand=True)],
            vertical_alignment=ft.CrossAxisAlignment.START,  # Align to top
            spacing=8,  # Reduced spacing
        )

    def analyze_image(self):
        try:
            detailed_prompt = """
            قم بتحليل صورة الفحص المختبري وقدم:
            1. قراءة القيم المختبرية الموجودة
            2. تحديد إذا كانت القيم طبيعية أم لا
            3. شرح مبسط لمعنى هذه النتائج
            4. أي توصيات عامة بناءً على النتائج 

            اريد النتيجة باللغة العربية
            """

            summary_prompt = """
            قم بتحليل صورة الفحص المختبري وقدم نتيجة مختصرة جداً (سطر أو سطرين) 
            تشير فقط إلى وجود أو عدم وجود مشاكل صحية واضحة.

            اريد النتيجة باللغة العربية
            """
            image_data = pathlib.Path(self.image_path).read_bytes()
            
            detailed_response = self.model_vision.generate_content(
                glm.Content(
                    parts=[
                        glm.Part(text=detailed_prompt),
                        glm.Part(
                            inline_data=glm.Blob(
                                mime_type='image/jpeg',
                                data=image_data
                            )
                        ),
                    ],
                ))
            self.detailed_analysis = detailed_response.text

            summary_response = self.model_vision.generate_content(
                glm.Content(
                    parts=[
                        glm.Part(text=summary_prompt),
                        glm.Part(
                            inline_data=glm.Blob(
                                mime_type='image/jpeg',
                                data=image_data
                            )
                        ),
                    ],
                ))

            return summary_response.text

        except Exception as e:
            print(f"Error in analyze_image: {str(e)}")
            # Don't raise here, return an error message instead
            return "حدث خطأ أثناء تحليل الصورة.  يرجى المحاولة مرة أخرى."

    def create_result_container(self, summary):
      return ft.Container(
        content=ft.Column([
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(
                            "النتيجة المختصرة:",
                            size=16,  # Consistent size
                            weight=ft.FontWeight.BOLD,
                            color="#004AAD",
                        ),
                        ft.Container(
                            content=ft.Text(
                                summary,
                                size=14,
                                color="black",
                            ),
                            padding=ft.padding.symmetric(vertical=8), # Reduced padding
                        ),
                        ft.ElevatedButton( # Button inside the card
                            "تحميل التقرير الكامل",
                            on_click=self.download_report,
                            style=ft.ButtonStyle(
                                bgcolor="#007BFF",
                                color="white",
                                padding=ft.padding.all(10), # Consistent padding
                                shape=ft.RoundedRectangleBorder(radius=8)
                            )
                        )
                    ]),
                    padding=ft.padding.all(15), # Consistent padding
                ),
               color="white", # White card background
                elevation=3,  # Subtle elevation

            ),
        ]),
        padding=ft.padding.only(top=10, bottom=10, left=20, right=20),  # Consistent padding
      )

    def create_pdf_report(self, detailed_analysis, filename="medical2_report.pdf"):
        doc = SimpleDocTemplate(
            filename,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )

        styles = getSampleStyleSheet()
        # Use a ParagraphStyle that supports Arabic and set alignment to right
        arabic_style = ParagraphStyle(
            'Arabic',
            fontName='Arabic',  # Make sure 'Arabic' font is registered
            fontSize=14,
            leading=20,  # Adjust leading as needed
            alignment=4,  # TA_JUSTIFY (4) for justified text
            rightIndent=20,
            leftIndent=20,
        )

        content = []
        # Reshape and display text for proper Arabic rendering
        title_text = get_display(arabic_reshaper.reshape("تقرير التحليل المخبري"))
        content.append(Paragraph(title_text, arabic_style))
        content.append(Spacer(1, 12))

        analysis_text = get_display(arabic_reshaper.reshape(detailed_analysis))
        content.append(Paragraph(analysis_text, arabic_style))

        doc.build(content)
        return filename

    def download_report(self, e):
        if self.detailed_analysis:
            try:
                report_path = self.create_pdf_report(self.detailed_analysis)
                self.add_message("AI", "تم إنشاء التقرير بنجاح! يمكنك العثور عليه في: " + report_path)
            except Exception as err:
                self.add_message("AI", f"حدث خطأ أثناء إنشاء التقرير: {str(err)}")
                print(f"Error in download_report: {str(err)}") # For debugging


    def pick_file(self, e):
        self.pick_files_dialog.pick_files(allowed_extensions=["png", "jpg", "jpeg"])

    def clear_chat(self, e):
        self.chat.controls.clear()
        self.page.update()

    def on_message(self, message):
        if hasattr(message, 'user_name') and hasattr(message, 'text'):
            self.add_message(message.user_name, message.text,
                           is_image=getattr(message, 'is_image', False))
class DoctorsView(ft.View):
    def __init__(self):
        super().__init__(
            route="/doctors",
            padding=ft.padding.only(left=0, right=0, bottom=0, top=0),
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            bgcolor="#E6F3F3"  # Consistent background
        )

        # Mock data (replace with your actual data source)
        self.doctors_data = [
            {"name": "د. أحمد علي", "phone": "+967 777 123 456", "specialty": "أخصائي قلب"},
            {"name": "د. فاطمة سالم", "phone": "+967 733 987 654", "specialty": "أخصائي أطفال"},
            {"name": "د. عمر حسن", "phone": "+967 711 555 222", "specialty": "أخصائي أعصاب"},
            {"name": "د. ليلى محمد", "phone": "+967 772 333 444", "specialty": "أخصائي جلدية"},
            {"name": "د. سامي يوسف", "phone": "+967 735 777 888", "specialty": "جراح عام"},
            {"name": "د. هدى إبراهيم", "phone": "+967 778 999 000", "specialty": "أخصائي عيون"},
            {"name": "د. خالد سعيد", "phone": "+967 712 444 555", "specialty": "جراح عظام"},
            {"name": "د. منى عبد الله", "phone": "+967 774 666 777", "specialty": "أخصائي أنف وأذن وحنجرة"},
            {"name": "د. رامي ناصر", "phone": "+967 736 888 999", "specialty": "أخصائي مسالك بولية"},
            {"name": "د. نور مصطفى", "phone": "+967 779 111 222", "specialty": "طبيب نفسي"},
        ]


        self.__header = ft.Container(
            content=ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        icon_color="#000000",
                        on_click=lambda e: e.page.go("/Splash")  # Back to main
                    ),
                   
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
             bgcolor="#87CEEB",  # Consistent header color
             padding=ft.padding.only(top=8)
        )


        self.__title = ft.Text(
            value="الأطباء",
            color=ft.colors.BLACK,
            size=22,
            font_family="Poppins",
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER
        )

        self.doctors_list = ft.Column(
            scroll=ft.ScrollMode.AUTO,  # Enable scrolling if needed
            controls=self.create_doctor_cards(),
            spacing=15,
            height=550,  # Set a fixed height for the scrollable area
        )

        self.__content = ft.Container(
            content=ft.Column(
                controls=[
                    self.__title,
                    ft.Divider(height=10, color=ft.colors.GREY_300),
                    self.doctors_list,

                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
            ),
            padding=20,  # Add padding around content
        )

        self.controls = [self.__header, self.__content]


    def create_doctor_cards(self):
        cards = []
        for doctor in self.doctors_data:
            card = ft.Card(
                elevation=4,
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.ListTile(
                                leading=ft.Icon(ft.icons.PERSON, size=40, color="#87CEEB"),
                                title=ft.Text(doctor["name"], size=18, weight=ft.FontWeight.BOLD),
                                subtitle=ft.Text(doctor["specialty"], size=14, color=ft.colors.GREY_700),
                                trailing= ft.IconButton(ft.icons.PHONE,icon_color="#87CEEB"), #  phone icon
                            ),
                             ft.Row([  # Display phone number under the name/specialty.  Better layout.
                                 # ft.Icon(ft.icons.PHONE, size=16, color=ft.colors.GREY_600), #Removed, it's redundant
                                 ft.Text(doctor["phone"], size=14, color=ft.colors.GREY_600)

                             ],
                             alignment=ft.MainAxisAlignment.CENTER
                            ),
                            ft.Divider(height=1, color=ft.colors.GREY_300), # Add dividers
                            
                        ],
                        spacing=5, # Reduce spacing within the card
                    ),
                    width=320,   # consistent width
                    padding=10,  # consistent padding
                    # bgcolor=ft.colors.WHITE, # Optional:  Make card background white
                    border_radius=ft.border_radius.all(10),  # Rounded corners for the card
                ),
                # margin=ft.margin.only(bottom=10) # Removed, as we're using spacing in Column

            )
            cards.append(card)
        return cards


class Settings(ft.View):
    def __init__(self):
        super().__init__(
            route="/settings",
            padding=ft.padding.only(left=0, right=0, bottom=0, top=0),
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            bgcolor="#E6F3F3"  # Same background as other views
        )
        # Assuming you have a BottomAppBar class (from your previous code)
        # self.bottom_appbar = BottomAppBar(page=self.page)

        self.__header = ft.Container(
            content=ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.HOME,
                        icon_color="#000000",
                        on_click=lambda e: e.page.go("/Splash")  
                        # on_click=lambda e: e.page.go("/Splash")  #  Navigation handled in main
                    ),
            
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            bgcolor="#87CEEB",  # Consistent header color
        )

        self.__title = ft.Text(
            value="الإعدادات",
            color=ft.colors.BLACK,
            size=22,
            font_family="Poppins",  # Consistent font
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER
        )

        # --- Example Settings (Design Only) ---

        # Language Selection
        self.language_dropdown = ft.Dropdown(
            options=[
                ft.dropdown.Option("العربية"),
                ft.dropdown.Option("English"),
            ],
            label="اللغة",
            width=200,
            # on_change=self.change_language  #  No event handling
        )

        # Theme Switch
        self.theme_switch = ft.Switch(label="الوضع الداكن", label_position=ft.LabelPosition.LEFT) # No event handling

        # Notifications Switch
        self.notifications_switch = ft.Switch(label="الإشعارات", label_position=ft.LabelPosition.LEFT) # No event handling

        # About and Version (using a Column for better layout)
        self.about = ft.Text("حول التطبيق...")
        self.version = ft.Text("الإصدار 1.0")
        self.about_section = ft.Column([self.about, self.version], alignment=ft.MainAxisAlignment.CENTER)


        # --- Layout ---

        self.__content = ft.Container(
            content=ft.Column(
                controls=[
                    self.__title,
                    ft.Divider(height=20, color=ft.colors.GREY_300), # Visual separation

                    # Language Setting
                    self.language_dropdown,

                    # Theme Setting
                    self.theme_switch,

                    # Notifications Setting
                    self.notifications_switch,

                    ft.Divider(height=20, color=ft.colors.GREY_300), # Visual separation

                    # About Section
                    self.about_section,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15, #Consistent spacing
            ),
            padding=20,  #  Padding
           # margin=ft.margin.only(top=20), #removed, no need
        )

        self.controls = [self.__header, self.__content]  # No bottom_appbar here, for demonstration
class ResultsView(ft.View):
    def __init__(self, results_data):
        super().__init__()
        self.route = "/results"
        self.scroll = ft.ScrollMode.ALWAYS
        self.results_data = results_data
        def format_arabic_text(text):
            reshaped_text = arabic_reshaper.reshape(text)
            bidi_text = get_display(reshaped_text)
            return bidi_text

        def generate_pdf(e):
            try:
                # تحديد مسار مجلد التنزيلات حسب نظام التشغيل
                if platform.system() == "Android":
                    downloads_path = "/storage/emulated/0/Download"
                else:
                    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")

                # التأكد من وجود المجلد
                if not os.path.exists(downloads_path):
                    os.makedirs(downloads_path)

                # تحديد مسار ملف الخط والتحقق من وجوده
                current_dir = os.path.dirname(__file__)
                font_path = os.path.join(current_dir, 'Amiri-Bold.ttf')
                
                if not os.path.exists(font_path):
                    raise FileNotFoundError(f"ملف الخط غير موجود في المسار: {font_path}")
                
                # تسجيل الخط العربي
                pdfmetrics.registerFont(TTFont('Arabic', font_path))
                
                # إنشاء اسم الملف مع الطابع الزمني
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                pdf_path = os.path.join(downloads_path, f'medical_report_{timestamp}.pdf')

                # إعداد مستند PDF
                doc = SimpleDocTemplate(
                    pdf_path,
                    pagesize=letter,
                    rightMargin=72,
                    leftMargin=72,
                    topMargin=72,
                    bottomMargin=72
                )

                # إعداد الأنماط
                styles = getSampleStyleSheet()
                arabic_style = ParagraphStyle(
                    'Arabic',
                    fontName='Arabic',
                    fontSize=14,
                    leading=16,
                    alignment=TA_RIGHT,
                    rtl=True
                )
                
                title_style = ParagraphStyle(
                    'ArabicTitle',
                    fontName='Arabic',
                    fontSize=18,
                    leading=22,
                    alignment=TA_RIGHT,
                    rtl=True
                )

                content = []
                
                # إضافة العنوان
                title_text = "تقرير التشخيص الطبي"
                content.append(Paragraph(title_text, title_style))
                content.append(Spacer(1, 20))

                # دالة مساعدة لإضافة الأقسام
                def add_section(title, text):
                    content.append(Paragraph(f"{title}: {text}", arabic_style))
                    content.append(Spacer(1, 12))

                # إضافة محتوى التقرير
                add_section("المرض المتوقع", self.results_data['disease'])
                add_section("الوصف", self.results_data['description'])
                add_section("الأعراض", '، '.join(self.results_data['symptoms']))
                add_section("الاحتياطات", '، '.join(self.results_data['precautions']))
                add_section("الأدوية", '، '.join(self.results_data['medications']))
                add_section("النظام الغذائي", '، '.join(self.results_data['diet']))
                add_section("التمارين", '، '.join(self.results_data['workout']))
                add_section("الفحوصات المختبرية", '، '.join(self.results_data['tests']))
                
                # إضافة التاريخ
                date_text = f"تاريخ التقرير: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                content.append(Spacer(1, 20))
                content.append(Paragraph(date_text, arabic_style))

                # بناء المستند
                doc.build(content)

                # عرض رسالة نجاح
                self.page.show_snack_bar(
                    ft.SnackBar(
                        content=ft.Text(f"تم حفظ التقرير في مجلد التنزيلات: medical_report_{timestamp}.pdf"),
                        action="حسناً"
                    )
                )

            except FileNotFoundError as e:
                error_message = f"لم يتم العثور على ملف الخط: {str(e)}"
                print(error_message)
                self.page.show_snack_bar(
                    ft.SnackBar(
                        content=ft.Text(error_message),
                        action="حسناً"
                    )
                )
            except Exception as e:
                error_message = f"حدث خطأ أثناء إنشاء التقرير: {str(e)}"
                print(error_message)
                self.page.show_snack_bar(
                    ft.SnackBar(
                        content=ft.Text(error_message),
                        action="حسناً"
                    )
                )

        self.controls = [
            ft.AppBar(
                leading=ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    on_click=lambda _: self.page.go("/Splash")
                ),
                title=ft.Text("نتائج التشخيص"),
                bgcolor="#87CEEB",
                center_title=True
            ),
            ft.Container(
                content=ft.Column(
                    scroll=ft.ScrollMode.ALWAYS,
                    controls=[
                        ft.Card(
                            content=ft.Container(
                                content=ft.ListTile(
                                    leading=ft.Icon(ft.icons.MEDICAL_SERVICES, color="#87CEEB"),
                                    title=ft.Text("المرض المتوقع", style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                                    subtitle=ft.Text(results_data['disease'])
                                ),
                                padding=10
                            )
                        ),
                        ft.Card(
                            content=ft.Container(
                                content=ft.ListTile(
                                    leading=ft.Icon(ft.icons.DESCRIPTION, color="#87CEEB"),
                                    title=ft.Text("الوصف", style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                                    subtitle=ft.Text(results_data['description'])
                                ),
                                padding=10
                            )
                        ),
                        ft.Card(
                            content=ft.Container(
                                content=ft.ListTile(
                                    leading=ft.Icon(ft.icons.HEALING, color="#87CEEB"),
                                    title=ft.Text("الأعراض", style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                                    subtitle=ft.Text(", ".join(results_data['symptoms']))
                                ),
                                padding=10
                            )
                        ),
                        ft.Card(
                            content=ft.Container(
                                content=ft.ListTile(
                                    leading=ft.Icon(ft.icons.WARNING, color="#87CEEB"),
                                    title=ft.Text("الاحتياطات", style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                                    subtitle=ft.Text(", ".join(results_data['precautions']))
                                ),
                                padding=10
                            )
                        ),
                        ft.Card(
                            content=ft.Container(
                                content=ft.ListTile(
                                    leading=ft.Icon(ft.icons.MEDICATION, color="#87CEEB"),
                                    title=ft.Text("الأدوية", style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                                    subtitle=ft.Text(", ".join(results_data['medications']))
                                ),
                                padding=10
                            )
                        ),
                        ft.Card(
                            content=ft.Container(
                                content=ft.ListTile(
                                    leading=ft.Icon(ft.icons.RESTAURANT_MENU, color="#87CEEB"),
                                    title=ft.Text("النظام الغذائي", style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                                    subtitle=ft.Text(", ".join(results_data['diet']))
                                ),
                                padding=10
                            )
                        ),
                        ft.Card(
                            content=ft.Container(
                                content=ft.ListTile(
                                    leading=ft.Icon(ft.icons.FITNESS_CENTER, color="#87CEEB"),
                                    title=ft.Text("التمارين", style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                                    subtitle=ft.Text(", ".join(results_data['workout']))
                                ),
                                padding=10
                            )
                        ),
                  ft.Card(
    content=ft.Container(
        content=ft.ListTile(
            leading=ft.Icon(ft.icons.SCIENCE, color="#87CEEB"),  # تم التصحيح
            title=ft.Text("الفحوصات المختبرية اللازمة", style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
            subtitle=ft.Text(results_data['tests'])
        ),
        padding=10
    )
),
                        # زر الطباعة
                        ft.Container(
                            content=ft.ElevatedButton(
                                "طباعة التقرير",
                                icon=ft.icons.PRINT,
                                on_click=generate_pdf,
                                style=ft.ButtonStyle(
                                    color="white",
                                    bgcolor="#87CEEB",
                                ),
                            ),
                            alignment=ft.alignment.center,
                            padding=20,
                        ),
                    ],
                    spacing=10
                ),
                padding=20,
                expand=True
            )
        ]

        # تعيين ارتفاع ثابت للحاوية
        self.height = 600

import flet as ft


class BottomAppBar(ft.BottomAppBar):
    def __init__(self, page: ft.Page):  # Add page as an argument
        super().__init__()
        self.page = page # Store the page instance
        self.height = 60
        self.bgcolor = "#87CEEB"
        self.shadow_color = ft.colors.BLACK
        self.elevation = 7
        self.padding = ft.padding.only(left=0, right=0, bottom=0, top=8)
        self.__bottom = ft.Container(
            height=55,
            bgcolor=ft.colors.WHITE,
            border_radius=ft.border_radius.only(top_left=30, top_right=30),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    self.__icon(ft.icons.HOME, True, "/Splash"),  # Home icon, selected by default, routes to "/"
                    self.__icon(ft.icons.HEALING, False, "/home"),  # Doctors icon, routes to "/doctors"
                    self.__icon(ft.icons.HEALING, False,"/home2"),
                     self.__icon(ft.icons.VERIFIED_USER, False ,"/doctors"), # #Settings
                    self.__icon(ft.icons.SETTINGS, False ,"/settings"), #Settings
                 
                ]
            )

        )

        self.content = self.__bottom

    def __icon(self, name: str, selected: bool = False, route: str = None) -> ft.IconButton:
        return ft.IconButton(
            data={"selected": selected, "route": route},
            icon=name,
            icon_color="#87CEEB" if selected else "#C1C1C1",
            icon_size=40,
            on_click=self.__clicked,
        )

    def __clicked(self, e: ft.ControlEvent) -> None:
        for i in e.control.parent.controls:
            i.data["selected"] = False  # Deselect all icons
            if i.data["selected"]: 
              i.icon_color = "#C1C1C1"

        e.control.data["selected"] = True  # Select the clicked icon
        e.control.icon_color = "#87CEEB"
        e.control.update()

        for i in e.control.parent.controls:
            if i.data["selected"]:
                i.icon_color = "#87CEEB"
            else:
                i.icon_color = "#C1C1C1"
            i.update() #update each icon

        if e.control.data["route"]:  # Check if the icon has a route
            e.page.go(e.control.data["route"])  # Navigate to the specified route
        e.page.update()



class Home2(ft.View):
    def __init__(self):
        super().__init__(
            route="/home2",
            padding=ft.padding.only(left=0, right=0, bottom=0, top=0),
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            bgcolor="#E6F3F3"
        )
        self.bottom_appbar = BottomAppBar(page=self.page)  

        self.__header = ft.Container(
            content=ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        icon_color="#000000",
                        on_click=lambda e: e.page.go("/Splash")  
                    ),
                    ft.Container(
                        content=ft.Image(
                            src="ai.jpg",
                            width=50,
                            height=50,
                        ),
                        expand=True,
                        alignment=ft.alignment.center,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            bgcolor="#87CEEB",
        )

        self.__title = ft.Text(
            value="اختر الأعراض التي تعاني منها",
            color=ft.colors.BLACK,
            size=22,
            font_family="Poppins",
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER
        )

        self.symptom_checkboxes = []
        arabic_symptoms = [k for k in symptoms_dict if isinstance(k, str) and not k.isascii()]

        symptom_controls = []
        for symptom in arabic_symptoms:
            checkbox = ft.Checkbox(label=symptom, value=False, label_position=ft.LabelPosition.LEFT)
            self.symptom_checkboxes.append(checkbox)

            symptom_container = ft.Container(
                content=checkbox,
                border=ft.border.all(1, ft.colors.GREY_400),
                border_radius=ft.border_radius.all(8),
                padding=ft.padding.all(10),
                alignment=ft.alignment.center_right,
                width=280,
            )
            symptom_controls.append(symptom_container)

        self.selected_symptoms_display = ft.Text("", text_align=ft.TextAlign.RIGHT)

        self.__submit_button = ft.ElevatedButton(
            text="تشخيص",
            style=ft.ButtonStyle(
                bgcolor="#87CEEB",
                color="black",
                shape=ft.RoundedRectangleBorder(radius=30),
            ),
            on_click=self.predict_disease,
            width=300,
            height=60
        )
        self.error_message = ft.Text("", color=ft.colors.RED)

        self.scrollable_symptoms = ft.Column(
            scroll=ft.ScrollMode.ALWAYS,
            controls=symptom_controls,
            height=300,
            horizontal_alignment=ft.CrossAxisAlignment.END,
            spacing=10,
        )

        self.__content = ft.Container(
            content=ft.Column(
                controls=[
                    self.__title,
                    self.scrollable_symptoms,
                    self.selected_symptoms_display,
                    self.__submit_button,
                    self.error_message

                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
            ),
            padding=10,
            margin=ft.margin.only(top=20),
        )

        self.controls = [self.__header, self.__content, self.bottom_appbar]


    def predict_disease(self, e):
        try:
            self.selected_symptoms = [
                cb.label for cb in self.symptom_checkboxes if cb.value
            ]

            if len(self.selected_symptoms) < 4:  
                self.page.show_dialog(
                    ft.AlertDialog(
                        modal=True,
                        title=ft.Text("عدد الأعراض غير كافٍ"),
                        content=ft.Text("للحصول على نتائج أكثر دقة، يرجى اختيار أربعة أعراض أو أكثر."),
                        actions=[
                            ft.TextButton("حسناً", on_click=lambda _: self.page.close_dialog()),
                        ],
                    )
                )
                return 

            predicted_disease = get_predicted_value(self.selected_symptoms)
            description, precautions, medications, diet, workout, tests = helper(predicted_disease)

            self.page.results_data = {
                "disease": predicted_disease,
                "description": description,
                "symptoms": self.selected_symptoms,
                "precautions": precautions,
                "medications": medications,
                "diet": diet,
                "workout": workout,
                "tests": tests,
            }
            self.page.go("/results")  # Move go() before update()
            self.error_message.value = ""

            for cb in self.symptom_checkboxes:
                cb.value = False
            self.selected_symptoms_display.value = ""
            self.page.update() # update after go() and resetting


        except Exception as e:
            print(f"Error: {str(e)}")
            self.page.show_dialog(    # Show error in a dialog
                ft.AlertDialog(
                    modal=True,
                    title=ft.Text("حدث خطأ"),
                    content=ft.Text(f"حدث خطأ: {str(e)}"),
                    actions=[
                        ft.TextButton("OK", on_click=lambda x: self.page.close_dialog())
                    ]
                )
            )
            self.update()


























