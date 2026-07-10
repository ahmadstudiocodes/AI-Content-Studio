class QualityRules:
    """
    Central Quality Rules
    Used by QualityEvaluator

    Each task has required sections
    with multiple accepted keywords.
    """


    RULES = {


        # ==============================
        # YouTube Agent
        # ==============================

        "youtube": {

            "required": {

                "title": [
                    "title",
                    "video title",
                    "عنوان",
                    "عنوان ویدیو",
                    "عنوان ویدئوی"
                ],


                "hook": [
                    "hook",
                    "شروع جذاب",
                    "قلاب",
                    "پیوند قوی",
                    "10 seconds",
                    "10 ثانیه",
                    "هوک"
                ],


                "structure": [
                    "structure",
                    "ساختار",
                    "زمان بندی",
                    "زمان‌بندی",
                    "timeline",
                    "video structure"
                ],


                "script": [
                    "script",
                    "سناریو",
                    "نریشن",
                    "outline",
                    "چکلیست نمایش",
                    "script outline"
                ],


                "thumbnail": [
                    "thumbnail",
                    "thumbnail concept",
                    "thumbnail design",
                    "تامبنیل",
                    "تصویر شاخص",
                    "تصویر اصلی",
                    "ایده تصویر",
                    "کاور"
                ],


                "seo": [
                    "seo",
                    "keywords",
                    "tags",
                    "کلمات کلیدی",
                    "کلیدواژه",
                    "برچسب",
                    "تگ"
                ]

            },


            "min_length": 400

        },



        # ==============================
        # Thumbnail Agent
        # ==============================

        "thumbnail": {


            "required": {


                "subject": [
                    "subject",
                    "موضوع",
                    "سوژه"
                ],


                "composition": [
                    "composition",
                    "ترکیب بندی",
                    "ترکیب‌بندی"
                ],


                "lighting": [
                    "lighting",
                    "نورپردازی",
                    "نور"
                ],


                "text": [
                    "text",
                    "thumbnail text",
                    "متن",
                    "نوشته"
                ]

            },


            "min_length": 150

        },



        # ==============================
        # Script Agent
        # ==============================

        "script": {


            "required": {


                "title": [
                    "title",
                    "عنوان"
                ],


                "hook": [
                    "hook",
                    "قلاب",
                    "شروع"
                ],


                "intro": [
                    "intro",
                    "مقدمه",
                    "شروع"
                ],


                "outro": [
                    "outro",
                    "پایان",
                    "call to action",
                    "cta"
                ]

            },


            "min_length": 500

        },



        # ==============================
        # Research Agent
        # ==============================

        "research": {


            "required": {


                "summary": [
                    "summary",
                    "خلاصه"
                ],


                "sources": [
                    "sources",
                    "منابع",
                    "reference",
                    "رفرنس"
                ]

            },


            "min_length": 600

        },



        # ==============================
        # Course Agent
        # ==============================

        "course": {


            "required": {


                "course title": [
                    "course title",
                    "عنوان دوره"
                ],


                "learning objectives": [
                    "learning objectives",
                    "اهداف یادگیری",
                    "هدف یادگیری"
                ]

            },


            "min_length": 500

        }

    }