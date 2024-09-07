# Stop all running containers
Write-Output "Stopping all running containers..."
docker stop $(docker ps -q) | Out-Null

# Remove all containers (both running and stopped)
Write-Output "Removing all containers..."
docker rm $(docker ps -a -q) | Out-Null

# Remove all images
Write-Output "Removing all images..."
docker rmi -f $(docker images -q) | Out-Null

# Remove all volumes
Write-Output "Removing all volumes..."
docker volume rm $(docker volume ls -q) | Out-Null

# Remove unused networks
Write-Output "Removing unused networks..."
docker network prune -f | Out-Null

# Prune system (includes containers, networks, images, and volumes)
Write-Output "Pruning the Docker system..."
docker system prune -a --volumes -f | Out-Null

Write-Output "Docker cleanup completed."
