from django.core.management.base import BaseCommand
from myApp.utils.predictor import train_model
from django.conf import settings

class Command(BaseCommand):
    help = '生成房价预测模型文件'

    def handle(self, *args,  ** options):
        train_model()
        self.stdout.write("模型文件已生成至: " + settings.MODEL_ROOT)