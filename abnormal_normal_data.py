from datetime import datetime, timedelta
gte=datetime(2023,5,1)
lt= gte+timedelta(days=30)
import calendar


all_images_qxr=ImageSeries.objects.filter(sourceID='5c_qxr_qmsk',created_at__gte=gte,created_at__lt=lt,usecase='qxr').order_by('created_at')
all_images_qmsk=ImageSeries.objects.filter(sourceID='5c_qxr_qmsk',created_at__gte=gte,created_at__lt=lt,usecase='qmsk').order_by('created_at')
all_images_qxr_valid=all_images_qxr.filter(is_valid=True).count()
all_images_qmsk_valid=all_images_qmsk.filter(is_valid=True).count()
all_images_qxr_invalid=all_images_qxr.filter(is_valid=False).count()
all_images_qmsk_invalid=all_images_qmsk.filter(is_valid=False).count()

imgs=ImageSeries.objects.filter(sourceID='5c_qxr_qmsk',created_at__gte=gte,created_at__lt=lt,usecase='qxr').values_list('id',flat=True)
imgqmsk=ImageSeries.objects.filter(sourceID='5c_qxr_qmsk',created_at__gte=gte,created_at__lt=lt,usecase='qmsk').values_list('id',flat=True)

from tqdm import tqdm

abnormal_count=0
normal_count=0
for img in tqdm(imgs):
    try:
        all_results=Result.objects.filter(image_series_id=img).values().last()['result_json']['tags']
        for all_result in all_results:
            if all_result['tag']=='abnormal' and all_result['presence']==True:
                abnormal_count= abnormal_count+1

            elif all_result['tag']=='abnormal' and all_result['presence']==False:
                normal_count= normal_count+1

    except:
        print('sdf')

print(f'abnormal-{abnormal_count} normal-{normal_count}')


from tqdm import tqdm

qmsk_abnormal_count=0
qmsk_normal_count=0
for img in tqdm(imgqmsk):
    try:
        all_results=Result.objects.filter(image_series_id=img).values().last()['result_json']['tags']
        for all_result in all_results:
            if all_result['tag']=='fracture' and all_result['presence']==True:
                qmsk_abnormal_count= qmsk_abnormal_count+1

            elif all_result['tag']=='fracture' and all_result['presence']==False:
                qmsk_normal_count= qmsk_normal_count+1

    except:
        print('sdf')
        
print(f"Total count for {calendar.month_name[gte.month]} Total qxr-{all_images_qxr.count()} valid qxr {all_images_qxr_valid} invalid qxr {all_images_qmsk_invalid} "
     f" qxr normal-{normal_count}"
     )
print(f"Total count for {calendar.month_name[gte.month]} "
      f"Total qmsk-{all_images_qmsk.count()} "
      f"valid qmsk {all_images_qmsk_valid} "
      f" invalid qmsk {all_images_qmsk_invalid} "
       f" qmsk fracture {qmsk_abnormal_count} "
     f" qmsk normal-{qmsk_normal_count}")

