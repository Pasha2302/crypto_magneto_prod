import redis
import json
import base64
from collections import Counter

# Подключение к Redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)

# Очереди, которые реально используются в настройках Celery
queues = ['default', 'heavy_tasks', 'fast_tasks', 'celery']

for queue_name in queues:
    queue_len = r.llen(queue_name)
    if queue_len == 0:
        print(f"🔍 Очередь '{queue_name}' пуста.\n")
        continue

    raw_tasks = r.lrange(queue_name, 0, queue_len - 1)
    counter = Counter()

    print(f"\n🔍 Очередь '{queue_name}': всего задач {queue_len}\n")

    for raw in raw_tasks:
        try:
            task_data = json.loads(raw)
            task_name = task_data['headers'].get('task')
            task_id = task_data['headers'].get('id')

            # Тело задачи закодировано в base64
            body_b64 = task_data['body']
            body_json = base64.b64decode(body_b64).decode('utf-8')
            args = json.loads(body_json)

            print(f"🟢 Задача: {task_name}")
            print(f"    ID: {task_id}")
            print(f"    args: {args}")
            print("-" * 60)

            counter[task_name] += 1

        except Exception as e:
            print(f"❌ Ошибка при разборе задачи в очереди '{queue_name}': {e}")
            print("-" * 60)

    print("\n📊 Сводка по типам задач в очереди:")
    for task, count in counter.items():
        print(f"   {task}: {count}")
    print("\n" + "=" * 80 + "\n")
