import numpy as np
from pyzbar import pyzbar
import cv2
import os
from PIL import Image, ImageDraw
from PIL import ImageEnhance
import pandas as pd

path1 = 'D:/test/img_all111' + "/"
dir_list = os.listdir(path1)
print(dir_list)
count = 0


def readbarcode():
    image_count = 0  # تتبع تسلسل الصور

    for file in dir_list:
        img1 = cv2.imread(f"{path1}" + f"{file}")

        # تحسين دقة الصورة
        img1 = cv2.resize(img1, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

        img1 = Image.fromarray(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))

        # زيادة التباين للصورة
        enhancer = ImageEnhance.Contrast(img1)
        img_contrast = enhancer.enhance(2.0)  # تحسين التباين بمعامل 2.0
        img1 = img_contrast

        barcodes = pyzbar.decode(img1)

        if len(barcodes) == 0:
            # دوران الصورة 360 درجة
            img_rotated = img1.rotate(360, expand=True)
            barcodes = pyzbar.decode(img_rotated)

            if len(barcodes) == 0:
                # لم يتم قراءة الباركود
                barcode_data = "غير مقروءة"
                barcode_orientation = None
            else:
                barcode = barcodes[0]
                barcode_data = barcode.data.decode("utf-8")
                barcode_orientation = barcode.orientation
        else:
            barcode = barcodes[0]
            barcode_data = barcode.data.decode("utf-8")
            barcode_orientation = barcode.orientation

        count += 1
        image_name = file

        # قراءة نص الباركود وتحديد حالته (مقروء أو غير مقروء)
        if barcode_data:
            barcode_status = "مقروء"
        else:
            barcode_status = "غير مقروء"

        data_list.append([image_name, barcode_data, barcode_orientation, barcode_status])

        # طباعة اسم الصورة وحالة الباركود وتسلسل الصورة ونتيجة قراءة الباركود ورقمه
        image_count += 1
        print(f"تسلسل الصورة: {image_count}")
        print(f"اسم الصورة: {image_name}")
        print(f"حالة الباركود: {barcode_status}")
        print(f"نتيجة قراءة الباركود: {barcode_data}")

    df = pd.DataFrame(data_list, columns=['اسم الصورة', 'بيانات الباركود', 'اتجاه الباركود', 'حالة الباركود'])
    df.loc[df['بيانات الباركود'] == 'غير مقروءة', 'حالة الباركود'] = 'غير مقروءة'
    excel_path = 'D:/eeeeee.xlsx'
    df.to_excel(excel_path, index=False)

    print(f"عدد الصور: {count}")
    print(f"تم حفظ ملف الإكسل في: {excel_path}")


readbarcode()
