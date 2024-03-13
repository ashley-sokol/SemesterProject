from django.test import TestCase
from workplace_violation_app.models import AnonReportInfo
from django.utils import timezone
from storages.backends.s3boto3 import S3Boto3Storage
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
import mock

# Create your tests here.
class AnonReportInfoTest(TestCase):
    def test_true(self):
        self.assertTrue(True)
    #def test_create_anon_report(self):
        """
        check if making an anon user works
        """
       # date = timezone.now().date()
       # text = "hi"
        #file= SimpleUploadedFile(
           # "best_file_eva.txt",
            #b"these are the file contents!"  # note the b in front of the string [bytes]
        #)
      #  AnonReportInfo.objects.create(report_date=date, report_text=text, report_file=file)
       # self.assertEquals(AnonReportInfo.objects.length, 1)


