from django.shortcuts import render
from .models import User, Task, Project, Entrance, Transaction, Done
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
import json
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

def landing(request):
    return render(request, 'landing.html')

def tasks(request):
    return render(request, 'tasks.html')

@csrf_exempt
def get_tasks(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            token = data.get('token')
            if not token:
                return JsonResponse({'error': 'Token not provided'}, status=400)

            user_e = User.objects.filter(token=token)
            user = user_e.first()
            if not user:
                return JsonResponse({'error': 'Invalid token'}, status=400)
            
            projects = Project.objects.filter(users__token=token)

            # tasks = Task.objects.filter(project__in=projects).values('id', 'name', 'project')
            # return JsonResponse(list(tasks), safe=False)
            result = {}
            for project in projects:
                tasks = Task.objects.filter(project=project).values('id', 'name')
                task_dict = {task['name']: task['id'] for task in tasks}
                result[project.name] = task_dict
            
            entrance = Entrance.objects.create()
            entrance.user.set(user_e)
            entrance.save()

            return JsonResponse(result, safe=False)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def add_task(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            task_name = data.get('task_name')
            project_name = data.get('project_name')
            
            if not task_name or not project_name:
                return HttpResponse(422)
            
            project = Project.objects.filter(name=project_name).first()
            
            if not project:
                return HttpResponse(404)
            
            task = Task.objects.create(name=task_name, project=project)

            transaction = Transaction.objects.create(action="Create")
            transaction.task.add(task)
            transaction.project.add(project)
            transaction.save()

            return JsonResponse({
                'task_id': task.id,
                'task_name': task.name,
                'project_name': project.name
            })
        
        except json.JSONDecodeError:
            return HttpResponse(400)
    
    return HttpResponse(405)
    
@csrf_exempt
def update_task(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            task_id = data.get('task_id')
            new_name = data.get('new_name')
            
            if not task_id or not new_name:
                return JsonResponse({'error': 'Task ID or new task name is missing'}, status=400)

            task = Task.objects.get(id=task_id)

            old_name = task.name
            
            task.name = new_name
            task.save()

            transaction = Transaction.objects.create(action=f"Rename from {old_name}")
            transaction.task.add(task)
            transaction.project.add(task.project)
            transaction.save()
            
            return JsonResponse({'success': 'Task name updated successfully'})
        
        except Task.DoesNotExist:
            return JsonResponse({'error': 'Task not found'}, status=404)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def delete_task(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            task_id = data.get('id')
            token = data.get('token')
            action = data.get('action')
            
            if not task_id or not token or not action:
                return JsonResponse({'error': 'Task ID, token or action is missing'}, status=400)
            
            user = User.objects.get(token=token)
            
            task = Task.objects.filter(id=task_id).first()
        
            if not task:
                return JsonResponse({'error': 'Task not found'}, status=404)
            
            transaction = Transaction.objects.create(action=f"Use {action}")
            transaction.task.add(task)
            transaction.project.add(task.project)
            transaction.save()

            if action == 'move_to_done':
                task.delete()
                done = Done.objects.create(name=task.name)
                done.user.add(user)
                return JsonResponse({'success': 'Task moved to Done successfully'})
            elif action == 'delete':
                task.delete()
                return JsonResponse({'success': 'Task deleted successfully'})
            else:
                return JsonResponse({'error': 'Invalid action'}, status=400)
        
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)