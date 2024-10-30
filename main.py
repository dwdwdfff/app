from kivy.lang import Builder
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivy.uix.image import Image
from kivy.core.window import Window
from datetime import datetime

KV = '''
BoxLayout:
    orientation: 'vertical'

    MDBoxLayout:
        size_hint_y: None
        height: '70dp'  # اجعل ارتفاع الجزء العلوي أكبر لإضافة الشعار
        padding: '10dp'
        spacing: '10dp'
        md_bg_color: [0.145, 0.588, 0.745, 1] 

        # Image للشعار
        Image:
            source: "logo.png"  # استبدل "logo.png" بمسار شعارك
            size_hint: (None, 1)
            size: ("110dp", "110dp")  # حجم الشعار
            allow_stretch: True

        # Label لعنوان العملة
        MDLabel:
            text: "Currency Exchange Rates"
            font_style: "H5"
            halign: "center"
            theme_text_color: "Custom"
            text_color: [1, 1, 1, 1]  # اللون الأبيض بال RGBA
            size_hint_x: 0.7  # استخدم جزء من المساحة
            valign: "middle"  # محاذاة عمودية في المنتصف
            text_size: self.size  # اجعل النص يتمدد إلى حجم الـ MDLabel

        # Label للوقت
        MDLabel:
            id: time_label
            text: "12:00 PM"  # الوقت الافتراضي
            font_style: "H5"
            halign: "right"
            theme_text_color: "Custom"
            size_hint_x: 0.3  # استخدم جزء من المساحة
            text_color: [1, 1, 1, 1]  # اللون الأبيض بال RGBA

    MDBoxLayout:
        size_hint_y: None
        height: '50dp'
        spacing: 2
        padding: [10, 5]
        md_bg_color: [1, 0.8, 0.06, 1]  # لون برتقالي فاتح بال RGBA

        MDLabel:
            text: "Currency"
            halign: "center"
            bold: True
            theme_text_color: "Custom"
            text_color: [0, 0, 0, 1]  # اللون الأسود بال RGBA
            size_hint_x: 0.4

        MDLabel:
            text: "Sell"
            halign: "center"
            bold: True
            theme_text_color: "Custom"
            text_color: [0, 0, 0, 1]  # اللون الأسود بال RGBA
            size_hint_x: 0.3000

        MDLabel:
            text: "Buy"
            halign: "center"
            bold: True
            theme_text_color: "Custom"
            text_color: [0, 0, 0, 1]  # اللون الأسود بال RGBA
            size_hint_x: 0.3

    ScrollView:
        MDBoxLayout:
            id: currency_box
            orientation: 'vertical'
            adaptive_height: True
            spacing: 10
            padding: [10, 10]
'''

class CurrencyRow(MDBoxLayout):
    def __init__(self, currency, buy_price, sell_price, image_path, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = '50dp'  # يمكنك تغيير ارتفاع المربعات هنا

        self.padding = [5, 5]
        self.spacing = 10

        # مربع العملة مع الصورة
        currency_card = MDCard(
            size_hint=(0.1, None),
            size=("230dp", "50dp"),
            md_bg_color=[0.69, 0.89, 0.98, 1],  # اللون الأزرق الفاتح بال RGBA
            elevation=2,
            radius=[10, 10, 10, 10]
        )
        
        currency_box = MDBoxLayout(orientation="horizontal", spacing=5, padding=[5, 0])
        currency_image = Image(
            source=image_path,
            size_hint=(None, None),
            size=("30dp", "30dp"),
            allow_stretch=True
        )
        currency_label = MDLabel(
            text=currency,
            halign="center",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1)
        )
        
        currency_box.add_widget(currency_image)
        currency_box.add_widget(currency_label)
        currency_card.add_widget(currency_box)
        self.add_widget(currency_card)

        # مربع سعر البيع
        sell_card = MDCard(
            size_hint=(0.12, None),
            size=("230dp", "50dp"),
            md_bg_color=[0.25, 0.69, 0.31, 1],  # اللون الأخضر بال RGBA
            elevation=2,
            radius=[10, 10, 10, 10]
        )

        sell_layout = MDBoxLayout(orientation='vertical', spacing=2)
        sell_label = MDLabel(
            text=str(sell_price),
            halign="center",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1)
        )
     
        sell_layout.add_widget(sell_label)
        sell_card.add_widget(sell_layout)
        self.add_widget(sell_card)

        # مربع سعر الشراء
        buy_card = MDCard(
            size_hint=(0.12, None),
            size=("300dp", "50dp"),
            md_bg_color=[149, 26, 26, 0.8],  # اللون الأحمر بال RGBA
            elevation=2,
            radius=[10, 10, 10, 10]
        )

        buy_layout = MDBoxLayout(orientation='vertical', spacing=2)
        buy_label = MDLabel(
            text=str(buy_price),
            halign="center",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1)
        )
      
        buy_layout.add_widget(buy_label)
        buy_card.add_widget(buy_layout)
        self.add_widget(buy_card)

class CurrencyApp(MDApp):
    def build(self):
        Window.size = (400, 600)
        self.theme_cls.primary_palette = "Amber"
        self.theme_cls.primary_hue = "700"
        self.root = Builder.load_string(KV)
        Clock.schedule_interval(self.update_currency_prices, 60)
        Clock.schedule_interval(self.update_time, 1)  # تحديث الوقت كل ثانية
        self.update_currency_prices()
        self.update_time()
        return self.root

    def update_currency_prices(self, *args):
        currencies = [
            {"currency": "USD/EGP", "buy": 3.64, "sell": 3.66, "image": "usd.png"},
            {"currency": "JOD/EGP", "buy": 5.14, "sell": 5.16, "image": "jod.png"},
            {"currency": "EUR/EGP", "buy": 3.88, "sell": 3.98, "image": "jod.png"},
            {"currency": "EGP/EGP", "buy": 0.10, "sell": 0.12, "image": "jod.png"},
            {"currency": "USD/EGP", "buy": 3.64, "sell": 3.66, "image": "jod.png"},
            {"currency": "JOD/EGP", "buy": 5.14, "sell": 5.16, "image": "jod.png"},
            {"currency": "EUR/EGP", "buy": 3.88, "sell": 3.98, "image": "jod.png"},
            {"currency": "EGP/EGP", "buy": 0.10, "sell": 0.12, "image": "jod.png"},
            {"currency": "JOD/EGP", "buy": 5.14, "sell": 5.16, "image": "jod.png"},
        ]

        self.root.ids.currency_box.clear_widgets()
        for currency_data in currencies:
            row = CurrencyRow(currency_data["currency"], currency_data["buy"], currency_data["sell"], currency_data["image"])
            self.root.ids.currency_box.add_widget(row)

    def update_time(self, *args):
        current_time = datetime.now()
        am_pm = "AM" if current_time.hour < 12 else "PM"
        hour = current_time.strftime("%I")  # 12-hour format
        minute = current_time.strftime("%M")
        formatted_time = f"{hour}:{minute} {am_pm}"
        self.root.ids.time_label.text = formatted_time

if __name__ == "__main__":
    CurrencyApp().run()




