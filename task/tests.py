from django.test import TestCase
from task.models import Task
from task.forms import NewTaskForm, UpdateTaskForm

class TestTaskModel(TestCase):
    def test_should_be_able_to_create_a_task_model(self):
        tasks = Task.objects.count()

        self.assertEqual(0, tasks)
    
    def test_should_return_string_representation_from_task_model(self):
        task = Task.objects.create(title="First task")

        self.assertEqual(task.title, str(task))

class TestIndexPage(TestCase):
    def setUp(self):      
        self.task = Task.objects.create(title="First task", description="description")
        
    def test_should_render_index_page_with_correct_response(self):
        url = "/"
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'task/listtask.html')
        self.assertEqual(200, response.status_code)
    
    def test_should_display_tasks_on_index_page(self):
        response = self.client.get('/')

        self.assertContains(response, self.task.title)

    def test_should_display_description_on_index_page(self):
        response = self.client.get('/')

        self.assertContains(response, self.task.description)

    def test_should_have_link_to_add_item(self):
        response = self.client.get('/')

        self.assertContains(response, "Add")
        self.assertContains(response, "<a href")

class TestDetailPage(TestCase):
    def setUp(self):      
        self.task = Task.objects.create(title="First task", description="The description")
        self.task2 = Task.objects.create(title="Second task", description="The description")

    def test_should_render_detail_page_with_correct_response(self):
        url = f"/{self.task.id}/"
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'task/detail.html')
        self.assertEqual(200, response.status_code)
    

    def test_should_display_task_on_detail_page(self):
        url = f"/{self.task.id}/"
        response = self.client.get(url)

        self.assertContains(response, self.task.title)
        self.assertContains(response, self.task.description)
        self.assertNotContains(response, self.task2.title)
    

class TestNewPage(TestCase):
    def setUp(self):
        self.form = NewTaskForm

    def test_should_render_new_page_with_correct_response(self):
        url = f"/new/"
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'task/new.html')
        self.assertEqual(response.status_code,200)

    def test_should_have_valid_form_in_new_page(self):
        self.assertTrue(issubclass(self.form, NewTaskForm))
        #check fields are in the meta
        self.assertTrue('description' in self.form.Meta.fields)
        self.assertTrue('title' in self.form.Meta.fields)
        
        #test valid form

        form = self.form({
            'title': 'The title',
            'description': 'The description'
        })
        
        self.assertTrue(form.is_valid())

    
    def test_should_display_form_in_new_page(self):
        url = f"/new/"
        response = self.client.get(url)

        self.assertContains(response, '<form')
        self.assertContains(response, 'csrfmiddlewaretoken')
        self.assertContains(response, '<label for')

    
    
    def test_should_save_new_task_when_data_is_valid_in_new_form(self):
        data = {
            'title': 'The title',
            'description': 'The description'
        }

        url = f"/new/"
        response = self.client.post(url, data)

        #cant use these because it redirects
        #self.assertNotContains(response, '<ul class="errorlist"')
        #self.assertNotContains(response, 'This field is required.')
        self.assertRedirects(response, expected_url='/')
        self.assertEqual(Task.objects.count(), 1)

class TestUpdatePage(TestCase):
    def setUp(self):
        self.task = Task.objects.create(title='First task')
        self.form = UpdateTaskForm

    
    def test_should_render_update_page_with_correct_response(self):
        url = f"/{self.task.id}/update/"
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'task/update.html')
        self.assertEqual(response.status_code,200)
    
    def test_should_have_valid_form_in_update_page(self):
        self.assertTrue(issubclass(self.form, UpdateTaskForm))
        #check fields are in the meta
        self.assertTrue('title' in self.form.Meta.fields)
        self.assertTrue('description' in self.form.Meta.fields)
        
        #test valid form
        #updates self.task with new data
        form = self.form({
            'title': 'The title',
            'description': 'The description'
        }, instance=self.task)
        
        self.assertTrue(form.is_valid())
        
        form.save()

        self.assertEqual(self.task.title, "The title")

    def test_should_be_invalid_when_title_is_empty(self):
        form = self.form({
            'title': '',
            'description': 'The description'
        }, instance=self.task)

        self.assertFalse(form.is_valid())
    
    def test_should_render_form_in_update_page(self):
        url = f"/{self.task.id}/update/"
        response = self.client.get(url)

        self.assertContains(response, '<form')
        self.assertContains(response, 'csrfmiddlewaretoken')
        self.assertContains(response, '<label for')
        self.assertContains(response, "First task")

    def test_should_render_error_when_title_is_blank_in_update_page(self):
        data = {
            'title': '',
            'description': 'The description'
        }

        url = f"/{self.task.id}/update/"
        response = self.client.post(url, data)

        self.assertContains(response, '<ul class="errorlist"')
        self.assertContains(response, 'This field is required.')

    def test_should_update_task_when_data_is_valid(self):
        data = {
            'title': 'The title',
            'description': 'The description'
        }

        url = f"/{self.task.id}/update/"
        response = self.client.post(url, data)

        #cant use these because it redirects
        #self.assertNotContains(response, '<ul class="errorlist"')
        #self.assertNotContains(response, 'This field is required.')
        self.assertRedirects(response, expected_url='/')
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.first().title, "The title")

class TestDeletePage(TestCase):
    def setUp(self):
        self.task = Task.objects.create(title='First task')

    def test_should_have_a_delete_page(self):
        pass

    def test_should_delete_task_on_delete_page(self):
        self.assertEqual(Task.objects.count(), 1)

        url = f"/{self.task.id}/delete/"
        response = self.client.post(url)

        self.assertRedirects(response, expected_url='/')
        self.assertEqual(Task.objects.count(), 0)