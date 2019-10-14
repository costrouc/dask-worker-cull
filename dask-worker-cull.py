import kubernetes
import logging

kubernetes.config.load_incluster_config()


def list_pods():
    api_client = kubernetes.client.CoreV1Api()
    response = api_client.list_pod_for_all_namespaces(watch=False)
    return [{'name': pod.metadata.name, 'namespace': pod.metadata.namespace, 'status': pod.status.phase} for pod in response.items]


def delete_pod(name, namespace):
    api_client = kubernetes.client.CoreV1Api()
    response = api_client.delete_namespaced_pod(name, namespace, body=kubernetes.client.V1DeleteOptions())
    return response


def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('dask-worker-cull')

    pods = list_pods()
    active_sessions = [pod for pod in pods if pod['name'].startswith('jupyter-')]
    usernames = [pod['name'][len('jupyter-'):] for pod in active_sessions]
    logger.info(f'{len(usernames)} active usernames: {usernames}')

    dask_workers = [pod for pod in pods if pod['name'].startswith('dask-')]
    logger.info(f'{len(dask_workers)} active dask workers')

    ghost_dask_workers = []
    for pod in dask_workers:
        for username in usernames:
            if pod['name'].startswith(f'dask-{username}-'):
                break
        else:
            ghost_dask_workers.append(pod)
    logger.info(f'{len(ghost_dask_workers)} ghost dask workers')

    for ghost_worker in ghost_dask_workers:
        logger.info(f"deleting ghost dask worker {ghost_worker['name']}")
        delete_pod(ghost_worker['name'], ghost_worker['namespace'])


if __name__ == "__main__":
    main()
