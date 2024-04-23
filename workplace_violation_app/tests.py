from io import StringIO
from sys import stdout

from django.template.loader import render_to_string
from django.test import TestCase, RequestFactory,Client
from django.http import Http404, response, HttpResponseRedirect
from django.core.exceptions import ValidationError
from unittest.mock import patch

from requests import Request
from workplace_violation_app.models import Report,CustomUser,CustomS3Storage
from workplace_violation_app.views import IndexView, UserSubmissionsTableView, SubmissionsTableView, ViewReportView
from django.urls import reverse


# https://docs.djangoproject.com/en/5.0/topics/testing/ SOURCE

#1. TESTING MODELS

#CustomUser model testing
class TestCustomUserModel(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username="testuser")
    #test to ensure we can successfully make a custom user (CustomUser model)
    def test_creating_user(self):
        self.assertEqual(len(CustomUser.objects.all()), 1)
        self.assertEqual(str(self.user), "testuser")
        self.assertFalse(self.user.is_admin)#default should be false

    #test to check is_admin field for CustomUser model
    def test_check_admin_user(self):
        self.user.is_admin=True
        self.assertTrue(self.user.is_admin)

#Report model testing
class TestReportModel(TestCase):
    def setUp(self):
        self.user=CustomUser.objects.create_user(username='testuser')
        self.report=Report.objects.create(
            report_user=self.user,
            report_date='2024-04-06',
            report_text='Test Report',
            report_status='New',
            admin_notes='Test Notes'
        )
    def test_create_report(self):
        self.assertEqual(str(self.report),f"Report from {self.report.report_date}")
        self.assertTrue(isinstance(self.report, Report))#check if report actually makes a Report model
        self.assertEqual(Report.objects.count(), 1)
        self.assertFalse(self.report.is_seen)#is_seen should be default Faulse
    def test_update_report_status(self):
        self.report.report_status='In Progress'
        self.assertEqual(self.report.report_status,'In Progress')
    def test_update_report_seen(self):
        self.report.is_seen = True
        self.assertTrue(self.report.is_seen)
    def test_changing_report_text(self):
        self.report.report_text='test report text'
        self.assertEqual(self.report.report_text,'test report text')

    def test_report_date(self):
        self.assertEqual(self.report.report_date, '2024-04-06')



#LoginView view testing
#set up for login testing
class TestLoginView(TestCase):
    def setUp(self):
        self.client=Client()
        self.view_url=reverse('workplace_violation_app:login')
    # def test_redirect(self):
    #     response = self.client.get(self.view_url)
    #     self.assertEqual(response.status_code, 200)

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
        response = self.client.get(reverse('workplace_violation_app:index'))
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('workplace_violation_app:index'))
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertEqual(response.status_code, 200)

#IndexView view testing
class IndexViewTest(TestCase):
    def setUp(self):
        self.view_url = reverse('workplace_violation_app:index')
    def test_redirect(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 200)
#UserReportView view testing
class UserReportViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.report = Report.objects.create(
            report_user=self.user,
            report_date='2024-04-14',
            report_text='Report by the user',
            report_status='New',
            admin_notes='Initial notes',
            report_number='4671197c-8447-4fbc-96fd-0e68cf77ac1d'
        )
        self.view_url = reverse('workplace_violation_app:user_report_view', kwargs={'report_number': self.report.report_number})

    def test_user_report_view_template(self):
        response = self.client.get(self.view_url)
        self.assertTemplateUsed(response, 'workplace_violation_app/user_report_view.html')

    def test_user_report_view_context(self):
        response = self.client.get(self.view_url)
        self.assertIn('report', response.context)
        self.assertEqual(response.context['report'].report_text, self.report.report_text)
        # Convert both dates to strings to compare(datetime.date obj and string)
        self.assertEqual(str(response.context['report'].report_date), str(self.report.report_date))

#ViewReportView view testing
class TestViewReportView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.report = Report.objects.create(
            report_user=self.user,
            report_date='2024-04-06',
            report_text='Test Report',
            report_status='New',
            admin_notes='Test Notes',
            report_number = '4671197c-8447-4fbc-96fd-0e68cf77ac1d'
        )
        self.view_url = reverse('workplace_violation_app:view_report',  kwargs={'report_number': self.report.report_number})
    def test_get_view_report(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'workplace_violation_app/view_report.html')

#SubmissionsTableView view testing
class SubmissionsTableViewTest(TestCase):
    def setUp(self):
        self.view_url = reverse('workplace_violation_app:submissions_table')
    def test_redirect(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 200)

#ReportActionView view testing
class ReportActionViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        Report.objects.create(report_user = self.user, report_number='4671197c-8447-4fbc-96fd-0e68cf77ac1d', report_text='Test Report', report_date='2024-04-06')
        self.report = Report.objects.get(report_number='4671197c-8447-4fbc-96fd-0e68cf77ac1d')
    def test_redirect(self):
        view_url = reverse('workplace_violation_app:view_action', kwargs={'report_number': self.report.report_number})
        response = self.client.get(view_url)
        self.assertEqual(response.status_code, 200)
    def test_standard_admin_notes(self):
        view_url = reverse('workplace_violation_app:view_action', kwargs={'report_number': self.report.report_number})
        response = self.client.get(view_url)
        self.assertIsNone(response.context['report'].admin_notes)
        self.assertEqual(response.status_code, 200)
        Report.objects.create(report_user = self.user, report_number='4671197c-8447-4fbc-96fd-0e68cf77ac1f', report_text='Test Report', report_date='2024-04-06', admin_notes = "test notes")
        self.report = Report.objects.get(report_number='4671197c-8447-4fbc-96fd-0e68cf77ac1f')
        view_url = reverse('workplace_violation_app:view_action', kwargs={'report_number': self.report.report_number})
        response = self.client.get(view_url)
        self.assertEqual(response.context['report'].admin_notes, "test notes")
        self.assertEqual(response.status_code, 200)

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












