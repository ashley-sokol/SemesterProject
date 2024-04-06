from io import StringIO
from sys import stdout

from django.test import TestCase, RequestFactory
from django.http import Http404, response
from django.core.exceptions import ValidationError
from unittest.mock import patch
from workplace_violation_app.models import Report
from workplace_violation_app.models import CustomUser
from workplace_violation_app.views import IndexView, UserSubmissionsTableView
from django.urls import reverse


# Create your tests here.
# https://docs.djangoproject.com/en/5.0/topics/testing/ SOURCE


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

class CaseSearch2(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.report = Report.objects.create(report_number='4671197c-8447-4fbc-96fd-0e68cf77ac1d', report_text='Test Report', report_date='2024-04-06')
    def test_valid_number(self):
        url = reverse('workplace_violation_app:index')
        data = {'search': 'search value', 'case_number': '4671197c-8447-4fbc-96fd-0e68cf77ac1d'}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)  # Check if the view returns a successful response
        self.assertTemplateUsed(response, 'workplace_violation_app/user_report_view.html')  # Check if the correct template is used
        self.assertIn('report', response.context)  # Check if the 'report' variable is in the context
        self.assertEqual(response.context['url'], reverse('workplace_violation_app:user_report_view', args=[self.report.pk]))  # Check if the URL is set correctly
        self.assertNotContains(response, "Form is not valid")  # Check if no error messages are displayed
    @patch('sys.stdout', new_callable=StringIO)
    def test_invalid_form(self, mock_stdout):
        url = reverse('workplace_violation_app:index')
        data = {'search': 'search value', 'case_number': ''}  # Missing case_number field to make the form invalid
        response = self.client.post(url, data)
        # Check if the error message is displayed in stdout
        self.assertIn("Form is not valid", mock_stdout.getvalue())
    @patch('sys.stdout', new_callable=StringIO)
    def test_nonexistent_case_number(self, mock_stdout):
        url = reverse('workplace_violation_app:index')
        data = {'search': 'search value', 'case_number': '4671197c-8447-4fbc-96rg-0e68cf77ac1d'}
        response = self.client.post(url, data)
        self.assertNotIn('report', response.context)  # Check if the 'report' variable is not in the context
        self.assertIn("Form is not valid", mock_stdout.getvalue())
    @patch('sys.stdout', new_callable=StringIO)
    def test_bad_format_case_number(self, mock_stdout):
        url = reverse('workplace_violation_app:index')
        data = {'search': 'search value', 'case_number': 'random-case-num47893'}
        response = self.client.post(url, data)
        self.assertNotIn('report', response.context)  # Check if the 'report' variable is not in the context
        self.assertIn("Form is not valid", mock_stdout.getvalue())

# class UserSubmissionsTableViewTest(TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#         self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
#         self.client.login(username='testuser', password='testpassword')
#         self.report = Report.objects.create(report_number='4671197c-8447-4fbc-96fd-0e68cf77ac1d',report_text='Test Report', report_date='2024-04-06')
#     def test_successful_no_file_path(self):
#         request = self.client.get('/user_submissions/')
#         response = UserSubmissionsTableView.as_view()(request)
#         self.assertTemplateUsed(response, 'workplace_violation_app/user_submissions.html')  # Check if the correct template is used
#         self.assertIn('submissions', response.context)
#         submissions = response.context['submissions']
#         self.assertEqual(len(submissions), 1)
class ReportInfoTest(TestCase):
    #practice test to ensure github actions is working. can delete later in the project
    def test_true(self):
        self.assertTrue(True)
    #def test_create_report(self):
        #Report.objects.create()
        #self.assertEquals(Report.objects.length, 1)

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


