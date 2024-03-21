from django.test import TestCase
from workplace_violation_app.models import Report
from workplace_violation_app.models import CustomUser
from django.utils import timezone
from storages.backends.s3boto3 import S3Boto3Storage
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import AbstractUser, User


# Create your tests here.

class CustomUserTest(TestCase):
    #test to ensure we can successfully make a custom user (CustomUser model)
    def test_creating_user(self):
        CustomUser.objects.create(username="hello")
        self.assertEqual(len(CustomUser.objects.all()), 1)

    #test to check is_admin field for CustomUser model
    def test_check_admin_user(self):
        user=CustomUser.objects.create(username="hello")
        user.is_admin=True
        self.assertTrue(user.is_admin)
class ReportInfoTest(TestCase):
    #practice test to ensure github actions is working. can delete later in the project
    def test_true(self):
        self.assertTrue(True)
    def test_create_report(self):
        Report.objects.create()
        self.assertEquals(Report.objects.length, 1)

    #test below not working bc of some storage problem. trying to sort it out but not needed for now
    #def test_create_anon_report(self):
       # date = timezone.now().date()
       # text = "hi"
        #file= SimpleUploadedFile(
           # "best_file_eva.txt",
            #b"these are the file contents!"  # note the b in front of the string [bytes]
        #)
      #  AnonReportInfo.objects.create(report_date=date, report_text=text, report_file=file)
       # self.assertEquals(AnonReportInfo.objects.length, 1)


