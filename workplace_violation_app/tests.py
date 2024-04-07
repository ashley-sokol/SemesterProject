from io import StringIO
from sys import stdout

from django.template.loader import render_to_string
from django.test import TestCase, RequestFactory,Client
from django.http import Http404, response, HttpResponseRedirect
from django.core.exceptions import ValidationError
from unittest.mock import patch
from workplace_violation_app.models import Report,CustomUser,CustomS3Storage
from workplace_violation_app.views import IndexView, UserSubmissionsTableView
from django.urls import reverse

# https://docs.djangoproject.com/en/5.0/topics/testing/ SOURCE

#1. TESTING MODELS

#CustomUser model testing
class TestCustomUserModel(TestCase):
    #test to ensure we can successfully make a custom user (CustomUser model)
    def test_creating_user(self):
        CustomUser.objects.create(username="hello")
        self.assertEqual(len(CustomUser.objects.all()), 1)

    #test to check is_admin field for CustomUser model
    def test_check_admin_user(self):
        user=CustomUser.objects.create(username="hello")
        user.is_admin=True
        self.assertTrue(user.is_admin)
#Customs3Storage model testing


#Report model testing
class TestReportModel(TestCase):
    def setUp(self):
        self.user=CustomUser.objects.create_user(username='testuser')
    def test_create_report(self):
       # storage=CustomS3Storage.objects.create()
        report=Report.objects.create(
            report_user=self.user,
            report_date='2024-04-06',
            report_text='Test Report',
            #report_file=storage,
            report_status='New',
            is_seen=False,
            admin_notes='Test Notes'
        )
        self.assertEqual(str(report),f"Report from {report.report_date}")
        self.assertTrue(isinstance(report, Report))#check if report actually makes a Report model
        #self.assertEqual(Report.objects.length, 1)

#LoginView view testing
#set up for login testing
class TestLoginView(TestCase):
    def setUp(self):
        self.client=Client()
        self.url=reverse('workplace_violation_app:login')

#Logout_view view testing
class LogoutViewTest(TestCase):
    #TODO: add assertions for user state
    def test_log_out_no_user(self):
        url = reverse('workplace_violation_app:logout')
        response = self.client.get(url)
        #ensure that valid html is returned
        self.assertEqual(response.status_code, 302)
    def test_log_out_custom_user(self):
        url = reverse('workplace_violation_app:logout')
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

#IndexView view testing

#UserReportView view testing

#ViewReportView view testing

#SubmissionsTableView view testing

#ReportActionView view testing

#UserSubmissionsTableView view testing
class TestUserSubmissionsTableView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        report = Report.objects.create(report_number='4671197c-8447-4fbc-96fd-0e68cf77ac1d',report_text='Test Report', report_date='2024-04-06')
        self.view_url = reverse('workplace_violation_app:user_submissions')
    @patch('sys.stdout', new_callable=StringIO)
    def test_successful_no_file_path(self, mock_stdout):
        request = self.factory.get(self.view_url)
        response = UserSubmissionsTableView.as_view()(request)
        self.assertIn("NO GIVEN FILE PATH", mock_stdout.getvalue())

#DeleteSubmission view testing
class TestDeleteSubmissionView(TestCase):
    def setUp(self):
        self.client=Client()
        self.url=reverse('workplace_violation_app:delete_submission')
    def test_delete_submission(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,405)


#case search tests
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












