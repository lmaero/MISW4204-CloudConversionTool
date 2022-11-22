# MISW4204-CloudConversionTool - Grupo 9

## Integrantes

- Diego Fernando Eslava Lozano
- Camilo Andrés Gálvez Vidal
- Alonso Daniel Cantú Trejo
- Luis Miguel Guzmán Pérez

## Sistema de Conversión Cloud - Escalabilidad en el Backend - Entrega 4

### Video de presentación del proyecto y resultados obtenidos
https://www.youtube.com/watch?v=9A8-IjI8iGg

### Paso a paso de reproducción del experimento


Para la ejecución correcta de los siguientes pasos, se espera que usted como usuario tenga instaladas las herramientas
necesarias en su máquina local: Postman. Así mismo se espera que tenga conocimientos de uso de la terminal y de Google
Cloud Console.

1. Ingresar a [Google Cloud Console](https://console.cloud.google.com), seleccione el proyecto **misw4204-grupo9** y
   abra el módulo Compute Engine - VM Instances. Verá la imagen a continuación con las instancias ejecutándose. En caso
   que no estén en ejecución, seleccionelas todas y presione el botón **Start** en el menú superior. 
   
   - En la primera imagen se muestran las VM instances del instance group web server, worker y notificator. Se desactivan las instancias de nfs-server que ahora se encuentra en un Cloud Storage, el web server, que ahora se encuentra como un instance group. El notificator se desactiva temporalmente para la ejecución de las pruebas de carga. 
   ![VMInsances](https://user-images.githubusercontent.com/26640034/201799917-40be6ff3-3d9f-4312-90e9-edcb6ee20a3c.jpg)


   - En la segunda imagen se muestra la instancia de SQL que está en una cuenta distinta de Google Cloud.
   ![SQLInstance](https://user-images.githubusercontent.com/60992168/199153040-f360a9ad-7e6a-4265-9fb6-783419d59991.jpeg)
   
   - En la tercera imagen se muestra la instancia usada para ejecutar pruebas de estrés con JMeter
   ![JMeter](https://user-images.githubusercontent.com/60992168/199153137-b856a885-d8f4-45bf-9afb-cbeea950a514.jpeg)
   
   - En la cuarta imagen se muestra la configuración de balanceador de cargas para el web server.
   ![LoadBalancing](https://user-images.githubusercontent.com/26640034/201800251-e8a28720-c0d5-4e2d-b939-7b6c19b0d9ac.jpg)
   
  - En la quinta imagen se muestra la configuración de las instancias de autoescalamiento a través de un instance group para el web server y la capa worker que permite operar varias VM idénticas. Eb la capa web server, se desplegaron dos instance group en dos regioens diferentes para beneficiar la disponibilidad. 
![InstanceGroups](https://user-images.githubusercontent.com/26640034/203232907-42637224-2627-4450-81f1-af819c6429f7.png)

  - En la sexta imagen se muestra la configuración de instance templates para la capa web server y la capa worker, que son las plantillas utilizadas para crear instancias de una VM y un instance group administrado.
![InstanceGroupTemplates](https://user-images.githubusercontent.com/26640034/203233226-5a29ad48-fb2e-498d-9e59-d537e32a66ec.png)

  - En la séptima imagen se muestra la configuración del Health Checker para verificar el estado de las VM creadas en el instance group y que estas respondan al tráfico de manera correcta.
![HealthCheck](https://user-images.githubusercontent.com/26640034/201801062-e9b5c31a-4b2d-498d-a149-031b94c284c0.jpg)

- En la octava imagen se muestra la configuración en Cloud Storage para el almacentamiento de los archivos de audio utilizados y que la App pueda acceder a ellos cuando lo necesite. En este caso se llama cloud-conversion-tool-bucket.
![Bucket](https://user-images.githubusercontent.com/26640034/203238022-d68f78a7-388f-46a6-9a65-f0ea674fb4ec.png)


- En la novena imagen se muestra que el proceso de autoescalamiento para la capa web server y la capa worker luego de realizar las pruebas de estrés del web server es satisfactorio. Se crearon dos nuevas instancias luego de copar el 80% de capacidad de la primera creada y luego de copar el 80% de la segunda creada.
![AutoscalingProcess](https://user-images.githubusercontent.com/26640034/203233450-2123104c-d7be-4a61-8a84-caf471229737.png)

- En la décima imagen se muestra la implementación del Pub/Sub, como sistema de comunicación entre la capa web server y worker de manera asíncrona. Se muestran los eventos generados en la ejecución de la aplicación.
![Pub/Sub](https://user-images.githubusercontent.com/26640034/203238097-b978ae56-fac5-46f2-aba6-88e7dd49a75d.png)

  
  Es importante mencionar que no se puede configurar el balanceador de cargas sin haber configurado previamente la opción de autoescalamiento. Además, ya bo se está utilizando el disco de arranque con las imágenes para ser utilizado por los instance group, si no las imágenes ahora son almacenadas en contenedores que se ejecutan de maenra automática cuando se realiza el proceso. 
  
  
2. Las instancias están configuradas para ejecutar los servicios haciendo uso de contenedores de Docker, abra una
   conexión SSH a cada una y verifique que se estén ejecutando correctamente con el siguiente comando.
   ```shell
   sudo docker ps -a
   ```
   
   - web-server (Docker container - estado) y worker (Docker container - estado)

   ![Webserver](https://user-images.githubusercontent.com/26640034/203234404-dfb72857-24a7-4586-bc8d-32ec5688afd3.png)
    ![Worker](https://user-images.githubusercontent.com/26640034/201802990-f6fb6727-d75e-47de-8556-e8f61d239240.jpeg)


3. En caso que alguno de los servicios contenerizados (web-server, worker, notificator) no se esté ejecutando:
   ![Screenshot from 2022-10-31 22-17-39](https://user-images.githubusercontent.com/60992168/199153519-4ea6ca20-bb51-460a-86cf-77d213698c7c.png)

   Iniciélos con los respectivos comandos a continuación:

    - web-server:
   ```shell
   sudo docker run -d -p 80:80 --env DEV_ENV=0 --env SQL_INSTANCE=34.71.15.212 --name web-server lmaerodev/misw4204-cloudconversiontool-web-server:v0.6.0
   ```
   

    - worker:
   ```shell
   sudo docker run -d -p 8000:8000 --env DEV_ENV=0 --env NOTIFICATOR_IP=10.128.0.10 --env NOTIFICATOR_PORT=7000 --name worker lmaerodev/misw4204-cloudconversiontool-worker:v0.5.0
   ```

    - notificator:
   ```shell
   sudo docker run -d -p 7000:7000 --name notificator lmaerodev/misw4204-cloudconversiontool-notificator:v0.4.0
   ```

4. El resultado de la ejecución de los comandos anteriores es el retorno del identificador del contenedor creado.
   Permita que los contenedores inicien sus servicios, este proceso tardará aproximadamente 1 minuto. Ejecute el comando
   del paso 3 nuevamente para verificar la correcta ejecución.
   
   ![Screenshot from 2022-10-31 22-21-50](https://user-images.githubusercontent.com/60992168/199153459-197f998b-10c1-4964-9c5c-a658de2b0d88.png)

5. Ejecute las colecciones de Postman a continuación.

## Ejecución de solicitudes - Postman

**Nota:** los escenarios están planteados para ser ejecutados una sola vez y en el orden planteado.

### Workspace de Postman - Público

[Postman Workspace](https://www.postman.com/lmaero-pro/workspace/misw4204-conversiontool)

### Colecciones para el Postman runner

Los botones a continuación le permiten hacer fork de las colecciones para ejecutarlas con el runner de Postman.
Asegúrese de seleccionar el environment GCloud.

Así mismo, en caso de que no desee ejecutarlas, puede verificar los resultados de la ejecución en el siguiente vínculo:
[Ir a escenarios de prueba ejecutados](https://github.com/lmaero/MISW4204-CloudConversionTool/wiki/Documentaci%C3%B3n-para-Usuarios#pruebas-api-postman)

#### 1 - /auth/signup

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/16367637-8e371886-137d-40fd-9ea8-0180a7108975?action=collection%2Ffork&collection-url=entityId%3D16367637-8e371886-137d-40fd-9ea8-0180a7108975%26entityType%3Dcollection%26workspaceId%3D5364826e-9d9b-40a6-bcb6-3976c612ccce#?env%5BDocker%5D=W3sia2V5IjoiUE9SVCIsInZhbHVlIjoiNjAwMCIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJkZWZhdWx0Iiwic2Vzc2lvblZhbHVlIjoiNjAwMCIsInNlc3Npb25JbmRleCI6MH0seyJrZXkiOiJVUkwiLCJ2YWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiZGVmYXVsdCIsInNlc3Npb25WYWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJzZXNzaW9uSW5kZXgiOjF9LHsia2V5IjoidmFsaWRfdXNlcm5hbWUiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjJ9LHsia2V5IjoidmFsaWRfcGFzc3dvcmQiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjN9LHsia2V5IjoicmVxdWVzdEJvZHkiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiJ7XCJ1c2VybmFtZVwiOlwiYWxvbnNvXCIsXCJlbWFpbFwiOlwiYS5jYW50dUB1bmlhbmRlcy5lZHUuY29cIixcInBhc3N3b3JkX2NvbmZpcm1hdGlvblwiOlwiMSMyM2w0RlwifSIsInNlc3Npb25JbmRleCI6NH0seyJrZXkiOiJ0b2tlbiIsInZhbHVlIjoiIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImFueSIsInNlc3Npb25WYWx1ZSI6IiIsInNlc3Npb25JbmRleCI6NX0seyJrZXkiOiJsb2NhbFRva2VuIiwidmFsdWUiOiIiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiYW55Iiwic2Vzc2lvblZhbHVlIjoiIiwic2Vzc2lvbkluZGV4Ijo2fV0=)

#### 2 - /auth/login

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/16367637-9de5e6fa-383a-4c06-a8d7-0124cde6a9b0?action=collection%2Ffork&collection-url=entityId%3D16367637-9de5e6fa-383a-4c06-a8d7-0124cde6a9b0%26entityType%3Dcollection%26workspaceId%3D5364826e-9d9b-40a6-bcb6-3976c612ccce#?env%5BDocker%5D=W3sia2V5IjoiUE9SVCIsInZhbHVlIjoiNjAwMCIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJkZWZhdWx0Iiwic2Vzc2lvblZhbHVlIjoiNjAwMCIsInNlc3Npb25JbmRleCI6MH0seyJrZXkiOiJVUkwiLCJ2YWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiZGVmYXVsdCIsInNlc3Npb25WYWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJzZXNzaW9uSW5kZXgiOjF9LHsia2V5IjoidmFsaWRfdXNlcm5hbWUiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjJ9LHsia2V5IjoidmFsaWRfcGFzc3dvcmQiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjN9LHsia2V5IjoicmVxdWVzdEJvZHkiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiJ7XCJ1c2VybmFtZVwiOlwiYWxvbnNvXCIsXCJlbWFpbFwiOlwiYS5jYW50dUB1bmlhbmRlcy5lZHUuY29cIixcInBhc3N3b3JkX2NvbmZpcm1hdGlvblwiOlwiMSMyM2w0RlwifSIsInNlc3Npb25JbmRleCI6NH0seyJrZXkiOiJ0b2tlbiIsInZhbHVlIjoiIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImFueSIsInNlc3Npb25WYWx1ZSI6IiIsInNlc3Npb25JbmRleCI6NX0seyJrZXkiOiJsb2NhbFRva2VuIiwidmFsdWUiOiIiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiYW55Iiwic2Vzc2lvblZhbHVlIjoiIiwic2Vzc2lvbkluZGV4Ijo2fV0=)

#### 3 - /tasks - POST

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/16367637-72352066-c2f8-42b4-849c-409c969e853b?action=collection%2Ffork&collection-url=entityId%3D16367637-72352066-c2f8-42b4-849c-409c969e853b%26entityType%3Dcollection%26workspaceId%3D5364826e-9d9b-40a6-bcb6-3976c612ccce#?env%5BDocker%5D=W3sia2V5IjoiUE9SVCIsInZhbHVlIjoiNjAwMCIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJkZWZhdWx0Iiwic2Vzc2lvblZhbHVlIjoiNjAwMCIsInNlc3Npb25JbmRleCI6MH0seyJrZXkiOiJVUkwiLCJ2YWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiZGVmYXVsdCIsInNlc3Npb25WYWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJzZXNzaW9uSW5kZXgiOjF9LHsia2V5IjoidmFsaWRfdXNlcm5hbWUiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjJ9LHsia2V5IjoidmFsaWRfcGFzc3dvcmQiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjN9LHsia2V5IjoicmVxdWVzdEJvZHkiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiJ7XCJ1c2VybmFtZVwiOlwiYWxvbnNvXCIsXCJlbWFpbFwiOlwiYS5jYW50dUB1bmlhbmRlcy5lZHUuY29cIixcInBhc3N3b3JkX2NvbmZpcm1hdGlvblwiOlwiMSMyM2w0RlwifSIsInNlc3Npb25JbmRleCI6NH0seyJrZXkiOiJ0b2tlbiIsInZhbHVlIjoiIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImFueSIsInNlc3Npb25WYWx1ZSI6IiIsInNlc3Npb25JbmRleCI6NX0seyJrZXkiOiJsb2NhbFRva2VuIiwidmFsdWUiOiIiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiYW55Iiwic2Vzc2lvblZhbHVlIjoiIiwic2Vzc2lvbkluZGV4Ijo2fV0=)

#### 4 - /tasks - GET

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/16367637-071a172c-d9d0-4d43-873e-cde499236216?action=collection%2Ffork&collection-url=entityId%3D16367637-071a172c-d9d0-4d43-873e-cde499236216%26entityType%3Dcollection%26workspaceId%3D5364826e-9d9b-40a6-bcb6-3976c612ccce#?env%5BDocker%5D=W3sia2V5IjoiUE9SVCIsInZhbHVlIjoiNjAwMCIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJkZWZhdWx0Iiwic2Vzc2lvblZhbHVlIjoiNjAwMCIsInNlc3Npb25JbmRleCI6MH0seyJrZXkiOiJVUkwiLCJ2YWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiZGVmYXVsdCIsInNlc3Npb25WYWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJzZXNzaW9uSW5kZXgiOjF9LHsia2V5IjoidmFsaWRfdXNlcm5hbWUiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjJ9LHsia2V5IjoidmFsaWRfcGFzc3dvcmQiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjN9LHsia2V5IjoicmVxdWVzdEJvZHkiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiJ7XCJ1c2VybmFtZVwiOlwiYWxvbnNvXCIsXCJlbWFpbFwiOlwiYS5jYW50dUB1bmlhbmRlcy5lZHUuY29cIixcInBhc3N3b3JkX2NvbmZpcm1hdGlvblwiOlwiMSMyM2w0RlwifSIsInNlc3Npb25JbmRleCI6NH0seyJrZXkiOiJ0b2tlbiIsInZhbHVlIjoiIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImFueSIsInNlc3Npb25WYWx1ZSI6IiIsInNlc3Npb25JbmRleCI6NX0seyJrZXkiOiJsb2NhbFRva2VuIiwidmFsdWUiOiIiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiYW55Iiwic2Vzc2lvblZhbHVlIjoiIiwic2Vzc2lvbkluZGV4Ijo2fV0=)

#### 5 - /tasks PUT

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/16367637-be8674c3-abcd-488e-985f-51a3a05568d1?action=collection%2Ffork&collection-url=entityId%3D16367637-be8674c3-abcd-488e-985f-51a3a05568d1%26entityType%3Dcollection%26workspaceId%3D5364826e-9d9b-40a6-bcb6-3976c612ccce#?env%5BDocker%5D=W3sia2V5IjoiUE9SVCIsInZhbHVlIjoiNjAwMCIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJkZWZhdWx0Iiwic2Vzc2lvblZhbHVlIjoiNjAwMCIsInNlc3Npb25JbmRleCI6MH0seyJrZXkiOiJVUkwiLCJ2YWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiZGVmYXVsdCIsInNlc3Npb25WYWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJzZXNzaW9uSW5kZXgiOjF9LHsia2V5IjoidmFsaWRfdXNlcm5hbWUiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjJ9LHsia2V5IjoidmFsaWRfcGFzc3dvcmQiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjN9LHsia2V5IjoicmVxdWVzdEJvZHkiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiJ7XCJ1c2VybmFtZVwiOlwiYWxvbnNvXCIsXCJlbWFpbFwiOlwiYS5jYW50dUB1bmlhbmRlcy5lZHUuY29cIixcInBhc3N3b3JkX2NvbmZpcm1hdGlvblwiOlwiMSMyM2w0RlwifSIsInNlc3Npb25JbmRleCI6NH0seyJrZXkiOiJ0b2tlbiIsInZhbHVlIjoiIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImFueSIsInNlc3Npb25WYWx1ZSI6IiIsInNlc3Npb25JbmRleCI6NX0seyJrZXkiOiJsb2NhbFRva2VuIiwidmFsdWUiOiIiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiYW55Iiwic2Vzc2lvblZhbHVlIjoiIiwic2Vzc2lvbkluZGV4Ijo2fV0=)

#### 6 - /files GET

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/16367637-84c8186c-37da-430c-b03d-47fe016f26ed?action=collection%2Ffork&collection-url=entityId%3D16367637-84c8186c-37da-430c-b03d-47fe016f26ed%26entityType%3Dcollection%26workspaceId%3D5364826e-9d9b-40a6-bcb6-3976c612ccce#?env%5BDocker%5D=W3sia2V5IjoiUE9SVCIsInZhbHVlIjoiNjAwMCIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJkZWZhdWx0Iiwic2Vzc2lvblZhbHVlIjoiNjAwMCIsInNlc3Npb25JbmRleCI6MH0seyJrZXkiOiJVUkwiLCJ2YWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiZGVmYXVsdCIsInNlc3Npb25WYWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJzZXNzaW9uSW5kZXgiOjF9LHsia2V5IjoidmFsaWRfdXNlcm5hbWUiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjJ9LHsia2V5IjoidmFsaWRfcGFzc3dvcmQiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjN9LHsia2V5IjoicmVxdWVzdEJvZHkiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiJ7XCJ1c2VybmFtZVwiOlwiYWxvbnNvXCIsXCJlbWFpbFwiOlwiYS5jYW50dUB1bmlhbmRlcy5lZHUuY29cIixcInBhc3N3b3JkX2NvbmZpcm1hdGlvblwiOlwiMSMyM2w0RlwifSIsInNlc3Npb25JbmRleCI6NH0seyJrZXkiOiJ0b2tlbiIsInZhbHVlIjoiIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImFueSIsInNlc3Npb25WYWx1ZSI6IiIsInNlc3Npb25JbmRleCI6NX0seyJrZXkiOiJsb2NhbFRva2VuIiwidmFsdWUiOiIiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiYW55Iiwic2Vzc2lvblZhbHVlIjoiIiwic2Vzc2lvbkluZGV4Ijo2fV0=)

#### 7 - /mail/send

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/16367637-ba57b3a9-b9b5-4bca-83c8-0ab7a44b8477?action=collection%2Ffork&collection-url=entityId%3D16367637-ba57b3a9-b9b5-4bca-83c8-0ab7a44b8477%26entityType%3Dcollection%26workspaceId%3D5364826e-9d9b-40a6-bcb6-3976c612ccce#?env%5BDocker%5D=W3sia2V5IjoiUE9SVCIsInZhbHVlIjoiNjAwMCIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJkZWZhdWx0Iiwic2Vzc2lvblZhbHVlIjoiNjAwMCIsInNlc3Npb25JbmRleCI6MH0seyJrZXkiOiJVUkwiLCJ2YWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiZGVmYXVsdCIsInNlc3Npb25WYWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJzZXNzaW9uSW5kZXgiOjF9LHsia2V5IjoidmFsaWRfdXNlcm5hbWUiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjJ9LHsia2V5IjoidmFsaWRfcGFzc3dvcmQiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjN9LHsia2V5IjoicmVxdWVzdEJvZHkiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiJ7XCJ1c2VybmFtZVwiOlwiYWxvbnNvXCIsXCJlbWFpbFwiOlwiYS5jYW50dUB1bmlhbmRlcy5lZHUuY29cIixcInBhc3N3b3JkX2NvbmZpcm1hdGlvblwiOlwiMSMyM2w0RlwifSIsInNlc3Npb25JbmRleCI6NH0seyJrZXkiOiJ0b2tlbiIsInZhbHVlIjoiIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImFueSIsInNlc3Npb25WYWx1ZSI6IiIsInNlc3Npb25JbmRleCI6NX0seyJrZXkiOiJsb2NhbFRva2VuIiwidmFsdWUiOiIiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiYW55Iiwic2Vzc2lvblZhbHVlIjoiIiwic2Vzc2lvbkluZGV4Ijo2fV0=)

#### 8 - /tasks DELETE

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/16367637-e920f4cd-34df-4318-b70e-a359dffdabe4?action=collection%2Ffork&collection-url=entityId%3D16367637-e920f4cd-34df-4318-b70e-a359dffdabe4%26entityType%3Dcollection%26workspaceId%3D5364826e-9d9b-40a6-bcb6-3976c612ccce#?env%5BDocker%5D=W3sia2V5IjoiUE9SVCIsInZhbHVlIjoiNjAwMCIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJkZWZhdWx0Iiwic2Vzc2lvblZhbHVlIjoiNjAwMCIsInNlc3Npb25JbmRleCI6MH0seyJrZXkiOiJVUkwiLCJ2YWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiZGVmYXVsdCIsInNlc3Npb25WYWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJzZXNzaW9uSW5kZXgiOjF9LHsia2V5IjoidmFsaWRfdXNlcm5hbWUiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjJ9LHsia2V5IjoidmFsaWRfcGFzc3dvcmQiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjN9LHsia2V5IjoicmVxdWVzdEJvZHkiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiJ7XCJ1c2VybmFtZVwiOlwiYWxvbnNvXCIsXCJlbWFpbFwiOlwiYS5jYW50dUB1bmlhbmRlcy5lZHUuY29cIixcInBhc3N3b3JkX2NvbmZpcm1hdGlvblwiOlwiMSMyM2w0RlwifSIsInNlc3Npb25JbmRleCI6NH0seyJrZXkiOiJ0b2tlbiIsInZhbHVlIjoiIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImFueSIsInNlc3Npb25WYWx1ZSI6IiIsInNlc3Npb25JbmRleCI6NX0seyJrZXkiOiJsb2NhbFRva2VuIiwidmFsdWUiOiIiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiYW55Iiwic2Vzc2lvblZhbHVlIjoiIiwic2Vzc2lvbkluZGV4Ijo2fV0=)


## Sistema de Conversión Cloud - Escalabilidad en la Capa Web - Entrega 3

### Video de presentación del proyecto y resultados obtenidos
https://www.youtube.com/watch?v=9A8-IjI8iGg

### Paso a paso de reproducción del experimento


Para la ejecución correcta de los siguientes pasos, se espera que usted como usuario tenga instaladas las herramientas
necesarias en su máquina local: Postman. Así mismo se espera que tenga conocimientos de uso de la terminal y de Google
Cloud Console.

1. Ingresar a [Google Cloud Console](https://console.cloud.google.com), seleccione el proyecto **misw4204-grupo9** y
   abra el módulo Compute Engine - VM Instances. Verá la imagen a continuación con las instancias ejecutándose. En caso
   que no estén en ejecución, seleccionelas todas y presione el botón **Start** en el menú superior. 
   
   - En la primera imagen se muestran las VM instances del instance group web server, worker y notificator. Se desactivan las instancias de nfs-server que ahora se encuentra en un Cloud Storage, el web server, que ahora se encuentra como un instance group. El notificator se desactiva temporalmente para la ejecución de las pruebas de carga. 
   ![VMInsances](https://user-images.githubusercontent.com/26640034/201799917-40be6ff3-3d9f-4312-90e9-edcb6ee20a3c.jpg)


   - En la segunda imagen se muestra la instancia de SQL que está en una cuenta distinta de Google Cloud.
   ![SQLInstance](https://user-images.githubusercontent.com/60992168/199153040-f360a9ad-7e6a-4265-9fb6-783419d59991.jpeg)
   
   - En la tercera imagen se muestra la instancia usada para ejecutar pruebas de estrés con JMeter
   ![JMeter](https://user-images.githubusercontent.com/60992168/199153137-b856a885-d8f4-45bf-9afb-cbeea950a514.jpeg)
   
   - En la cuarta imagen se muestra la configuración de balanceador de cargas para el web server.
   ![LoadBalancing](https://user-images.githubusercontent.com/26640034/201800251-e8a28720-c0d5-4e2d-b939-7b6c19b0d9ac.jpg)
   

  - En la quinta imagen se muestra la configuración de las instancias de autoescalamiento a través de un instance group para el web server que permite operar varias VM idénticas.
   ![InstanceGroup](https://user-images.githubusercontent.com/26640034/201800396-6fd175a1-555c-4aec-b883-664cfc8088e8.jpg)

  - En la sexta imagen se muestra la configuración de instance templates, que son las plantillas utilizadas para crear instancias de una VM y un instance group administrado.
![InstanceTemplate](https://user-images.githubusercontent.com/26640034/201800709-3af54171-b2a3-48c3-9586-eb04195cfedc.jpg)

  - En la séptima imagen se muestra la configuración del Health Checker para verificar el estado de las VM creadas en el instance group y que estas respondan al tráfico de manera correcta.
![HealthCheck](https://user-images.githubusercontent.com/26640034/201801062-e9b5c31a-4b2d-498d-a149-031b94c284c0.jpg)

- En la octava imagen se muestra la configuración de las imágenes de los discos de arranque para las VM instances de web server creadas en el instance group y que estas se encuentren creadas idénticamente.
![Images](https://user-images.githubusercontent.com/26640034/201801491-ac7a39d6-afa8-4192-a7ab-5a05e29dd4c7.jpg)

- En la novena imagen se muestra la configuración en Cloud Storage para el almacentamiento de los archivos de audio utilizados y que la App pueda acceder a ellos cuando lo necesite. En este caso se llama cloud-conversion-tool-bucket.
![ConversionToolBucket](https://user-images.githubusercontent.com/26640034/201801737-ba2dc127-c3eb-46c8-9bb7-e621b29b227e.jpg)

- En la décima imagen se muestra que el proceso de autoescalamiento luego de realizar las pruebas de estrés del web server es satisfactorio. Se crearon dos nuevas instancias luego de copar el 80% de capacidad de la primera creada y luego de copar el 80% de la segunda creada.
![Autoscaling](https://user-images.githubusercontent.com/26640034/201809051-8c054e89-ed31-4dc5-946e-1c866293d212.jpeg)

  
  Es importante mencionar que no se puede configurar el balanceador de cargas sin haber configurado previamente la opción de autoescalamiento.
  
  
2. Las instancias están configuradas para ejecutar los servicios haciendo uso de contenedores de Docker, abra una
   conexión SSH a cada una y verifique que se estén ejecutando correctamente con el siguiente comando.
   ```shell
   sudo docker ps -a
   ```
   
   - web-server (Docker container - estado) y worker (Docker container - estado)
    ![WebServer](https://user-images.githubusercontent.com/26640034/201802956-aea1ac79-5597-4226-b1a1-62265451b755.jpg) 
    ![Worker](https://user-images.githubusercontent.com/26640034/201802990-f6fb6727-d75e-47de-8556-e8f61d239240.jpeg)


3. En caso que alguno de los servicios contenerizados (web-server, worker, notificator) no se esté ejecutando:
   ![Screenshot from 2022-10-31 22-17-39](https://user-images.githubusercontent.com/60992168/199153519-4ea6ca20-bb51-460a-86cf-77d213698c7c.png)

   Iniciélos con los respectivos comandos a continuación:

    - web-server:
   ```shell
   sudo docker run -d -p 80:80 --env DEV_ENV=0 --env SQL_INSTANCE=34.71.15.212 --name web-server lmaerodev/misw4204-cloudconversiontool-web-server:v0.6.0
   ```
   

    - worker:
   ```shell
   sudo docker run -d -p 8000:8000 --env DEV_ENV=0 --env NOTIFICATOR_IP=10.128.0.10 --env NOTIFICATOR_PORT=7000 --name worker lmaerodev/misw4204-cloudconversiontool-worker:v0.5.0
   ```

    - notificator:
   ```shell
   sudo docker run -d -p 7000:7000 --name notificator lmaerodev/misw4204-cloudconversiontool-notificator:v0.4.0
   ```

4. El resultado de la ejecución de los comandos anteriores es el retorno del identificador del contenedor creado.
   Permita que los contenedores inicien sus servicios, este proceso tardará aproximadamente 1 minuto. Ejecute el comando
   del paso 3 nuevamente para verificar la correcta ejecución.
   
   ![Screenshot from 2022-10-31 22-21-50](https://user-images.githubusercontent.com/60992168/199153459-197f998b-10c1-4964-9c5c-a658de2b0d88.png)

5. Ejecute las colecciones de Postman a continuación.

## Ejecución de solicitudes - Postman

**Nota:** los escenarios están planteados para ser ejecutados una sola vez y en el orden planteado.

### Workspace de Postman - Público

[Postman Workspace](https://www.postman.com/lmaero-pro/workspace/misw4204-conversiontool)

### Colecciones para el Postman runner

Los botones a continuación le permiten hacer fork de las colecciones para ejecutarlas con el runner de Postman.
Asegúrese de seleccionar el environment GCloud.

Así mismo, en caso de que no desee ejecutarlas, puede verificar los resultados de la ejecución en el siguiente vínculo:
[Ir a escenarios de prueba ejecutados](https://github.com/lmaero/MISW4204-CloudConversionTool/wiki/Documentaci%C3%B3n-para-Usuarios#pruebas-api-postman)

#### 1 - /auth/signup

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/16367637-8e371886-137d-40fd-9ea8-0180a7108975?action=collection%2Ffork&collection-url=entityId%3D16367637-8e371886-137d-40fd-9ea8-0180a7108975%26entityType%3Dcollection%26workspaceId%3D5364826e-9d9b-40a6-bcb6-3976c612ccce#?env%5BDocker%5D=W3sia2V5IjoiUE9SVCIsInZhbHVlIjoiNjAwMCIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJkZWZhdWx0Iiwic2Vzc2lvblZhbHVlIjoiNjAwMCIsInNlc3Npb25JbmRleCI6MH0seyJrZXkiOiJVUkwiLCJ2YWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiZGVmYXVsdCIsInNlc3Npb25WYWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJzZXNzaW9uSW5kZXgiOjF9LHsia2V5IjoidmFsaWRfdXNlcm5hbWUiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjJ9LHsia2V5IjoidmFsaWRfcGFzc3dvcmQiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjN9LHsia2V5IjoicmVxdWVzdEJvZHkiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiJ7XCJ1c2VybmFtZVwiOlwiYWxvbnNvXCIsXCJlbWFpbFwiOlwiYS5jYW50dUB1bmlhbmRlcy5lZHUuY29cIixcInBhc3N3b3JkX2NvbmZpcm1hdGlvblwiOlwiMSMyM2w0RlwifSIsInNlc3Npb25JbmRleCI6NH0seyJrZXkiOiJ0b2tlbiIsInZhbHVlIjoiIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImFueSIsInNlc3Npb25WYWx1ZSI6IiIsInNlc3Npb25JbmRleCI6NX0seyJrZXkiOiJsb2NhbFRva2VuIiwidmFsdWUiOiIiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiYW55Iiwic2Vzc2lvblZhbHVlIjoiIiwic2Vzc2lvbkluZGV4Ijo2fV0=)

#### 2 - /auth/login

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/16367637-9de5e6fa-383a-4c06-a8d7-0124cde6a9b0?action=collection%2Ffork&collection-url=entityId%3D16367637-9de5e6fa-383a-4c06-a8d7-0124cde6a9b0%26entityType%3Dcollection%26workspaceId%3D5364826e-9d9b-40a6-bcb6-3976c612ccce#?env%5BDocker%5D=W3sia2V5IjoiUE9SVCIsInZhbHVlIjoiNjAwMCIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJkZWZhdWx0Iiwic2Vzc2lvblZhbHVlIjoiNjAwMCIsInNlc3Npb25JbmRleCI6MH0seyJrZXkiOiJVUkwiLCJ2YWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiZGVmYXVsdCIsInNlc3Npb25WYWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJzZXNzaW9uSW5kZXgiOjF9LHsia2V5IjoidmFsaWRfdXNlcm5hbWUiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjJ9LHsia2V5IjoidmFsaWRfcGFzc3dvcmQiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjN9LHsia2V5IjoicmVxdWVzdEJvZHkiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiJ7XCJ1c2VybmFtZVwiOlwiYWxvbnNvXCIsXCJlbWFpbFwiOlwiYS5jYW50dUB1bmlhbmRlcy5lZHUuY29cIixcInBhc3N3b3JkX2NvbmZpcm1hdGlvblwiOlwiMSMyM2w0RlwifSIsInNlc3Npb25JbmRleCI6NH0seyJrZXkiOiJ0b2tlbiIsInZhbHVlIjoiIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImFueSIsInNlc3Npb25WYWx1ZSI6IiIsInNlc3Npb25JbmRleCI6NX0seyJrZXkiOiJsb2NhbFRva2VuIiwidmFsdWUiOiIiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiYW55Iiwic2Vzc2lvblZhbHVlIjoiIiwic2Vzc2lvbkluZGV4Ijo2fV0=)

#### 3 - /tasks - POST

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/16367637-72352066-c2f8-42b4-849c-409c969e853b?action=collection%2Ffork&collection-url=entityId%3D16367637-72352066-c2f8-42b4-849c-409c969e853b%26entityType%3Dcollection%26workspaceId%3D5364826e-9d9b-40a6-bcb6-3976c612ccce#?env%5BDocker%5D=W3sia2V5IjoiUE9SVCIsInZhbHVlIjoiNjAwMCIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJkZWZhdWx0Iiwic2Vzc2lvblZhbHVlIjoiNjAwMCIsInNlc3Npb25JbmRleCI6MH0seyJrZXkiOiJVUkwiLCJ2YWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiZGVmYXVsdCIsInNlc3Npb25WYWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJzZXNzaW9uSW5kZXgiOjF9LHsia2V5IjoidmFsaWRfdXNlcm5hbWUiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjJ9LHsia2V5IjoidmFsaWRfcGFzc3dvcmQiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjN9LHsia2V5IjoicmVxdWVzdEJvZHkiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiJ7XCJ1c2VybmFtZVwiOlwiYWxvbnNvXCIsXCJlbWFpbFwiOlwiYS5jYW50dUB1bmlhbmRlcy5lZHUuY29cIixcInBhc3N3b3JkX2NvbmZpcm1hdGlvblwiOlwiMSMyM2w0RlwifSIsInNlc3Npb25JbmRleCI6NH0seyJrZXkiOiJ0b2tlbiIsInZhbHVlIjoiIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImFueSIsInNlc3Npb25WYWx1ZSI6IiIsInNlc3Npb25JbmRleCI6NX0seyJrZXkiOiJsb2NhbFRva2VuIiwidmFsdWUiOiIiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiYW55Iiwic2Vzc2lvblZhbHVlIjoiIiwic2Vzc2lvbkluZGV4Ijo2fV0=)

#### 4 - /tasks - GET

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/16367637-071a172c-d9d0-4d43-873e-cde499236216?action=collection%2Ffork&collection-url=entityId%3D16367637-071a172c-d9d0-4d43-873e-cde499236216%26entityType%3Dcollection%26workspaceId%3D5364826e-9d9b-40a6-bcb6-3976c612ccce#?env%5BDocker%5D=W3sia2V5IjoiUE9SVCIsInZhbHVlIjoiNjAwMCIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJkZWZhdWx0Iiwic2Vzc2lvblZhbHVlIjoiNjAwMCIsInNlc3Npb25JbmRleCI6MH0seyJrZXkiOiJVUkwiLCJ2YWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiZGVmYXVsdCIsInNlc3Npb25WYWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJzZXNzaW9uSW5kZXgiOjF9LHsia2V5IjoidmFsaWRfdXNlcm5hbWUiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjJ9LHsia2V5IjoidmFsaWRfcGFzc3dvcmQiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjN9LHsia2V5IjoicmVxdWVzdEJvZHkiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiJ7XCJ1c2VybmFtZVwiOlwiYWxvbnNvXCIsXCJlbWFpbFwiOlwiYS5jYW50dUB1bmlhbmRlcy5lZHUuY29cIixcInBhc3N3b3JkX2NvbmZpcm1hdGlvblwiOlwiMSMyM2w0RlwifSIsInNlc3Npb25JbmRleCI6NH0seyJrZXkiOiJ0b2tlbiIsInZhbHVlIjoiIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImFueSIsInNlc3Npb25WYWx1ZSI6IiIsInNlc3Npb25JbmRleCI6NX0seyJrZXkiOiJsb2NhbFRva2VuIiwidmFsdWUiOiIiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiYW55Iiwic2Vzc2lvblZhbHVlIjoiIiwic2Vzc2lvbkluZGV4Ijo2fV0=)

#### 5 - /tasks PUT

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/16367637-be8674c3-abcd-488e-985f-51a3a05568d1?action=collection%2Ffork&collection-url=entityId%3D16367637-be8674c3-abcd-488e-985f-51a3a05568d1%26entityType%3Dcollection%26workspaceId%3D5364826e-9d9b-40a6-bcb6-3976c612ccce#?env%5BDocker%5D=W3sia2V5IjoiUE9SVCIsInZhbHVlIjoiNjAwMCIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJkZWZhdWx0Iiwic2Vzc2lvblZhbHVlIjoiNjAwMCIsInNlc3Npb25JbmRleCI6MH0seyJrZXkiOiJVUkwiLCJ2YWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiZGVmYXVsdCIsInNlc3Npb25WYWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJzZXNzaW9uSW5kZXgiOjF9LHsia2V5IjoidmFsaWRfdXNlcm5hbWUiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjJ9LHsia2V5IjoidmFsaWRfcGFzc3dvcmQiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjN9LHsia2V5IjoicmVxdWVzdEJvZHkiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiJ7XCJ1c2VybmFtZVwiOlwiYWxvbnNvXCIsXCJlbWFpbFwiOlwiYS5jYW50dUB1bmlhbmRlcy5lZHUuY29cIixcInBhc3N3b3JkX2NvbmZpcm1hdGlvblwiOlwiMSMyM2w0RlwifSIsInNlc3Npb25JbmRleCI6NH0seyJrZXkiOiJ0b2tlbiIsInZhbHVlIjoiIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImFueSIsInNlc3Npb25WYWx1ZSI6IiIsInNlc3Npb25JbmRleCI6NX0seyJrZXkiOiJsb2NhbFRva2VuIiwidmFsdWUiOiIiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiYW55Iiwic2Vzc2lvblZhbHVlIjoiIiwic2Vzc2lvbkluZGV4Ijo2fV0=)

#### 6 - /files GET

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/16367637-84c8186c-37da-430c-b03d-47fe016f26ed?action=collection%2Ffork&collection-url=entityId%3D16367637-84c8186c-37da-430c-b03d-47fe016f26ed%26entityType%3Dcollection%26workspaceId%3D5364826e-9d9b-40a6-bcb6-3976c612ccce#?env%5BDocker%5D=W3sia2V5IjoiUE9SVCIsInZhbHVlIjoiNjAwMCIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJkZWZhdWx0Iiwic2Vzc2lvblZhbHVlIjoiNjAwMCIsInNlc3Npb25JbmRleCI6MH0seyJrZXkiOiJVUkwiLCJ2YWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiZGVmYXVsdCIsInNlc3Npb25WYWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJzZXNzaW9uSW5kZXgiOjF9LHsia2V5IjoidmFsaWRfdXNlcm5hbWUiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjJ9LHsia2V5IjoidmFsaWRfcGFzc3dvcmQiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjN9LHsia2V5IjoicmVxdWVzdEJvZHkiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiJ7XCJ1c2VybmFtZVwiOlwiYWxvbnNvXCIsXCJlbWFpbFwiOlwiYS5jYW50dUB1bmlhbmRlcy5lZHUuY29cIixcInBhc3N3b3JkX2NvbmZpcm1hdGlvblwiOlwiMSMyM2w0RlwifSIsInNlc3Npb25JbmRleCI6NH0seyJrZXkiOiJ0b2tlbiIsInZhbHVlIjoiIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImFueSIsInNlc3Npb25WYWx1ZSI6IiIsInNlc3Npb25JbmRleCI6NX0seyJrZXkiOiJsb2NhbFRva2VuIiwidmFsdWUiOiIiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiYW55Iiwic2Vzc2lvblZhbHVlIjoiIiwic2Vzc2lvbkluZGV4Ijo2fV0=)

#### 7 - /mail/send

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/16367637-ba57b3a9-b9b5-4bca-83c8-0ab7a44b8477?action=collection%2Ffork&collection-url=entityId%3D16367637-ba57b3a9-b9b5-4bca-83c8-0ab7a44b8477%26entityType%3Dcollection%26workspaceId%3D5364826e-9d9b-40a6-bcb6-3976c612ccce#?env%5BDocker%5D=W3sia2V5IjoiUE9SVCIsInZhbHVlIjoiNjAwMCIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJkZWZhdWx0Iiwic2Vzc2lvblZhbHVlIjoiNjAwMCIsInNlc3Npb25JbmRleCI6MH0seyJrZXkiOiJVUkwiLCJ2YWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiZGVmYXVsdCIsInNlc3Npb25WYWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJzZXNzaW9uSW5kZXgiOjF9LHsia2V5IjoidmFsaWRfdXNlcm5hbWUiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjJ9LHsia2V5IjoidmFsaWRfcGFzc3dvcmQiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjN9LHsia2V5IjoicmVxdWVzdEJvZHkiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiJ7XCJ1c2VybmFtZVwiOlwiYWxvbnNvXCIsXCJlbWFpbFwiOlwiYS5jYW50dUB1bmlhbmRlcy5lZHUuY29cIixcInBhc3N3b3JkX2NvbmZpcm1hdGlvblwiOlwiMSMyM2w0RlwifSIsInNlc3Npb25JbmRleCI6NH0seyJrZXkiOiJ0b2tlbiIsInZhbHVlIjoiIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImFueSIsInNlc3Npb25WYWx1ZSI6IiIsInNlc3Npb25JbmRleCI6NX0seyJrZXkiOiJsb2NhbFRva2VuIiwidmFsdWUiOiIiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiYW55Iiwic2Vzc2lvblZhbHVlIjoiIiwic2Vzc2lvbkluZGV4Ijo2fV0=)

#### 8 - /tasks DELETE

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/16367637-e920f4cd-34df-4318-b70e-a359dffdabe4?action=collection%2Ffork&collection-url=entityId%3D16367637-e920f4cd-34df-4318-b70e-a359dffdabe4%26entityType%3Dcollection%26workspaceId%3D5364826e-9d9b-40a6-bcb6-3976c612ccce#?env%5BDocker%5D=W3sia2V5IjoiUE9SVCIsInZhbHVlIjoiNjAwMCIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJkZWZhdWx0Iiwic2Vzc2lvblZhbHVlIjoiNjAwMCIsInNlc3Npb25JbmRleCI6MH0seyJrZXkiOiJVUkwiLCJ2YWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiZGVmYXVsdCIsInNlc3Npb25WYWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJzZXNzaW9uSW5kZXgiOjF9LHsia2V5IjoidmFsaWRfdXNlcm5hbWUiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjJ9LHsia2V5IjoidmFsaWRfcGFzc3dvcmQiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjN9LHsia2V5IjoicmVxdWVzdEJvZHkiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiJ7XCJ1c2VybmFtZVwiOlwiYWxvbnNvXCIsXCJlbWFpbFwiOlwiYS5jYW50dUB1bmlhbmRlcy5lZHUuY29cIixcInBhc3N3b3JkX2NvbmZpcm1hdGlvblwiOlwiMSMyM2w0RlwifSIsInNlc3Npb25JbmRleCI6NH0seyJrZXkiOiJ0b2tlbiIsInZhbHVlIjoiIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImFueSIsInNlc3Npb25WYWx1ZSI6IiIsInNlc3Npb25JbmRleCI6NX0seyJrZXkiOiJsb2NhbFRva2VuIiwidmFsdWUiOiIiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiYW55Iiwic2Vzc2lvblZhbHVlIjoiIiwic2Vzc2lvbkluZGV4Ijo2fV0=)


## Despliegue básico en nube pública - Entrega 2

### Video de presentación del proyecto y resultados obtenidos

### Paso a paso de reproducción del experimento
https://user-images.githubusercontent.com/60992168/199161568-d737829c-62dd-4739-98d3-d8606ed7d13f.mp4


Para la ejecución correcta de los siguientes pasos, se espera que usted como usuario tenga instaladas las herramientas
necesarias en su máquina local: Postman. Así mismo se espera que tenga conocimientos de uso de la terminal y de Google
Cloud Console.

1. Ingresar a [Google Cloud Console](https://console.cloud.google.com), seleccione el proyecto **misw4204-grupo9** y
   abra el módulo Compute Engine - VM Instances. Verá la imagen a continuación con las instancias ejecutándose. En caso
   que no estén en ejecución, seleccionelas todas y presione el botón **Start** en el menú superior.

    - En la primera imagen se muestran las VM instances del web-server, worker, nfs-server y notificator.
      ![Screenshot from 2022-10-31 21-59-48](https://user-images.githubusercontent.com/60992168/199153015-cb09f8d0-d6f9-420e-bffd-889cc74d5cef.png)

    - En la segunda imagen se muestra la instancia de SQL que está en una cuenta distinta de Google Cloud.
      ![SQLInstance](https://user-images.githubusercontent.com/60992168/199153040-f360a9ad-7e6a-4265-9fb6-783419d59991.jpeg)

    - En la tercera imagen se muestra la instancia usada para ejecutar pruebas de estrés con JMeter
      ![JMeter](https://user-images.githubusercontent.com/60992168/199153137-b856a885-d8f4-45bf-9afb-cbeea950a514.jpeg)

2. Las instancias están configuradas para ejecutar los servicios haciendo uso de contenedores de Docker, abra una
   conexión SSH a cada una y verifique que se estén ejecutando correctamente con el siguiente comando.
   ```shell
   sudo docker ps -a
   ```

    - NFS Server (reglas de firewall) y notificator (Docker container - estado)
      ![Screenshot from 2022-10-31 22-16-13](https://user-images.githubusercontent.com/60992168/199153205-7b087d76-575c-48e4-8469-7f98c02d1c39.png)

    - web-server (Docker container - estado) y worker (Docker container - estado)
      ![Screenshot from 2022-10-31 22-16-41](https://user-images.githubusercontent.com/60992168/199153372-ea7663ee-2a2c-4348-a6a4-0ff8caba6e33.png)

3. En caso que alguno de los servicios contenerizados (web-server, worker, notificator) no se esté ejecutando:
   ![Screenshot from 2022-10-31 22-17-39](https://user-images.githubusercontent.com/60992168/199153519-4ea6ca20-bb51-460a-86cf-77d213698c7c.png)

   Iniciélos con los respectivos comandos a continuación:

    - web-server:
   ```shell
   sudo docker run -d -p 80:80 -v /app/files:/app/files --name web-server lmaerodev/misw4204-cloudconversiontool-web-server:v0.4.0
   ```

    - worker:
   ```shell
   sudo docker run -d -p 8000:8000 -v /app/files:/app/files --env NOTIFICATOR_IP=10.128.0.10 --env NOTIFICATOR_PORT=7000 --name worker lmaerodev/misw4204-cloudconversiontool-worker:v0.4.0
   ```

    - notificator:
   ```shell
   sudo docker run -d -p 7000:7000 -v /app/files:/app/files --name notificator lmaerodev/misw4204-cloudconversiontool-notificator:v0.3.0
   ```

4. El resultado de la ejecución de los comandos anteriores es el retorno del identificador del contenedor creado.
   Permita que los contenedores inicien sus servicios, este proceso tardará aproximadamente 1 minuto. Ejecute el comando
   del paso 3 nuevamente para verificar la correcta ejecución.

   ![Screenshot from 2022-10-31 22-21-50](https://user-images.githubusercontent.com/60992168/199153459-197f998b-10c1-4964-9c5c-a658de2b0d88.png)

5. Ejecute las colecciones de Postman a continuación.

## Ejecución de solicitudes - Postman

**Nota:** los escenarios están planteados para ser ejecutados una sola vez y en el orden planteado.

### Workspace de Postman - Público

[Postman Workspace](https://www.postman.com/lmaero-pro/workspace/misw4204-conversiontool)

### Colecciones para el Postman runner

Los botones a continuación le permiten hacer fork de las colecciones para ejecutarlas con el runner de Postman.
Asegúrese de seleccionar el environment GCloud.

Así mismo, en caso de que no desee ejecutarlas, puede verificar los resultados de la ejecución en el siguiente vínculo:
[Ir a escenarios de prueba ejecutados](https://github.com/lmaero/MISW4204-CloudConversionTool/wiki/Documentaci%C3%B3n-para-Usuarios#pruebas-api-postman)

#### 1 - /auth/signup

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/16367637-8e371886-137d-40fd-9ea8-0180a7108975?action=collection%2Ffork&collection-url=entityId%3D16367637-8e371886-137d-40fd-9ea8-0180a7108975%26entityType%3Dcollection%26workspaceId%3D5364826e-9d9b-40a6-bcb6-3976c612ccce#?env%5BDocker%5D=W3sia2V5IjoiUE9SVCIsInZhbHVlIjoiNjAwMCIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJkZWZhdWx0Iiwic2Vzc2lvblZhbHVlIjoiNjAwMCIsInNlc3Npb25JbmRleCI6MH0seyJrZXkiOiJVUkwiLCJ2YWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiZGVmYXVsdCIsInNlc3Npb25WYWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJzZXNzaW9uSW5kZXgiOjF9LHsia2V5IjoidmFsaWRfdXNlcm5hbWUiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjJ9LHsia2V5IjoidmFsaWRfcGFzc3dvcmQiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjN9LHsia2V5IjoicmVxdWVzdEJvZHkiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiJ7XCJ1c2VybmFtZVwiOlwiYWxvbnNvXCIsXCJlbWFpbFwiOlwiYS5jYW50dUB1bmlhbmRlcy5lZHUuY29cIixcInBhc3N3b3JkX2NvbmZpcm1hdGlvblwiOlwiMSMyM2w0RlwifSIsInNlc3Npb25JbmRleCI6NH0seyJrZXkiOiJ0b2tlbiIsInZhbHVlIjoiIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImFueSIsInNlc3Npb25WYWx1ZSI6IiIsInNlc3Npb25JbmRleCI6NX0seyJrZXkiOiJsb2NhbFRva2VuIiwidmFsdWUiOiIiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiYW55Iiwic2Vzc2lvblZhbHVlIjoiIiwic2Vzc2lvbkluZGV4Ijo2fV0=)

#### 2 - /auth/login

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/16367637-9de5e6fa-383a-4c06-a8d7-0124cde6a9b0?action=collection%2Ffork&collection-url=entityId%3D16367637-9de5e6fa-383a-4c06-a8d7-0124cde6a9b0%26entityType%3Dcollection%26workspaceId%3D5364826e-9d9b-40a6-bcb6-3976c612ccce#?env%5BDocker%5D=W3sia2V5IjoiUE9SVCIsInZhbHVlIjoiNjAwMCIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJkZWZhdWx0Iiwic2Vzc2lvblZhbHVlIjoiNjAwMCIsInNlc3Npb25JbmRleCI6MH0seyJrZXkiOiJVUkwiLCJ2YWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiZGVmYXVsdCIsInNlc3Npb25WYWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJzZXNzaW9uSW5kZXgiOjF9LHsia2V5IjoidmFsaWRfdXNlcm5hbWUiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjJ9LHsia2V5IjoidmFsaWRfcGFzc3dvcmQiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjN9LHsia2V5IjoicmVxdWVzdEJvZHkiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiJ7XCJ1c2VybmFtZVwiOlwiYWxvbnNvXCIsXCJlbWFpbFwiOlwiYS5jYW50dUB1bmlhbmRlcy5lZHUuY29cIixcInBhc3N3b3JkX2NvbmZpcm1hdGlvblwiOlwiMSMyM2w0RlwifSIsInNlc3Npb25JbmRleCI6NH0seyJrZXkiOiJ0b2tlbiIsInZhbHVlIjoiIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImFueSIsInNlc3Npb25WYWx1ZSI6IiIsInNlc3Npb25JbmRleCI6NX0seyJrZXkiOiJsb2NhbFRva2VuIiwidmFsdWUiOiIiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiYW55Iiwic2Vzc2lvblZhbHVlIjoiIiwic2Vzc2lvbkluZGV4Ijo2fV0=)

#### 3 - /tasks - POST

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/16367637-72352066-c2f8-42b4-849c-409c969e853b?action=collection%2Ffork&collection-url=entityId%3D16367637-72352066-c2f8-42b4-849c-409c969e853b%26entityType%3Dcollection%26workspaceId%3D5364826e-9d9b-40a6-bcb6-3976c612ccce#?env%5BDocker%5D=W3sia2V5IjoiUE9SVCIsInZhbHVlIjoiNjAwMCIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJkZWZhdWx0Iiwic2Vzc2lvblZhbHVlIjoiNjAwMCIsInNlc3Npb25JbmRleCI6MH0seyJrZXkiOiJVUkwiLCJ2YWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiZGVmYXVsdCIsInNlc3Npb25WYWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJzZXNzaW9uSW5kZXgiOjF9LHsia2V5IjoidmFsaWRfdXNlcm5hbWUiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjJ9LHsia2V5IjoidmFsaWRfcGFzc3dvcmQiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjN9LHsia2V5IjoicmVxdWVzdEJvZHkiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiJ7XCJ1c2VybmFtZVwiOlwiYWxvbnNvXCIsXCJlbWFpbFwiOlwiYS5jYW50dUB1bmlhbmRlcy5lZHUuY29cIixcInBhc3N3b3JkX2NvbmZpcm1hdGlvblwiOlwiMSMyM2w0RlwifSIsInNlc3Npb25JbmRleCI6NH0seyJrZXkiOiJ0b2tlbiIsInZhbHVlIjoiIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImFueSIsInNlc3Npb25WYWx1ZSI6IiIsInNlc3Npb25JbmRleCI6NX0seyJrZXkiOiJsb2NhbFRva2VuIiwidmFsdWUiOiIiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiYW55Iiwic2Vzc2lvblZhbHVlIjoiIiwic2Vzc2lvbkluZGV4Ijo2fV0=)

#### 4 - /tasks - GET

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/16367637-071a172c-d9d0-4d43-873e-cde499236216?action=collection%2Ffork&collection-url=entityId%3D16367637-071a172c-d9d0-4d43-873e-cde499236216%26entityType%3Dcollection%26workspaceId%3D5364826e-9d9b-40a6-bcb6-3976c612ccce#?env%5BDocker%5D=W3sia2V5IjoiUE9SVCIsInZhbHVlIjoiNjAwMCIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJkZWZhdWx0Iiwic2Vzc2lvblZhbHVlIjoiNjAwMCIsInNlc3Npb25JbmRleCI6MH0seyJrZXkiOiJVUkwiLCJ2YWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiZGVmYXVsdCIsInNlc3Npb25WYWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJzZXNzaW9uSW5kZXgiOjF9LHsia2V5IjoidmFsaWRfdXNlcm5hbWUiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjJ9LHsia2V5IjoidmFsaWRfcGFzc3dvcmQiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjN9LHsia2V5IjoicmVxdWVzdEJvZHkiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiJ7XCJ1c2VybmFtZVwiOlwiYWxvbnNvXCIsXCJlbWFpbFwiOlwiYS5jYW50dUB1bmlhbmRlcy5lZHUuY29cIixcInBhc3N3b3JkX2NvbmZpcm1hdGlvblwiOlwiMSMyM2w0RlwifSIsInNlc3Npb25JbmRleCI6NH0seyJrZXkiOiJ0b2tlbiIsInZhbHVlIjoiIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImFueSIsInNlc3Npb25WYWx1ZSI6IiIsInNlc3Npb25JbmRleCI6NX0seyJrZXkiOiJsb2NhbFRva2VuIiwidmFsdWUiOiIiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiYW55Iiwic2Vzc2lvblZhbHVlIjoiIiwic2Vzc2lvbkluZGV4Ijo2fV0=)

#### 5 - /tasks PUT

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/16367637-be8674c3-abcd-488e-985f-51a3a05568d1?action=collection%2Ffork&collection-url=entityId%3D16367637-be8674c3-abcd-488e-985f-51a3a05568d1%26entityType%3Dcollection%26workspaceId%3D5364826e-9d9b-40a6-bcb6-3976c612ccce#?env%5BDocker%5D=W3sia2V5IjoiUE9SVCIsInZhbHVlIjoiNjAwMCIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJkZWZhdWx0Iiwic2Vzc2lvblZhbHVlIjoiNjAwMCIsInNlc3Npb25JbmRleCI6MH0seyJrZXkiOiJVUkwiLCJ2YWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiZGVmYXVsdCIsInNlc3Npb25WYWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJzZXNzaW9uSW5kZXgiOjF9LHsia2V5IjoidmFsaWRfdXNlcm5hbWUiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjJ9LHsia2V5IjoidmFsaWRfcGFzc3dvcmQiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjN9LHsia2V5IjoicmVxdWVzdEJvZHkiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiJ7XCJ1c2VybmFtZVwiOlwiYWxvbnNvXCIsXCJlbWFpbFwiOlwiYS5jYW50dUB1bmlhbmRlcy5lZHUuY29cIixcInBhc3N3b3JkX2NvbmZpcm1hdGlvblwiOlwiMSMyM2w0RlwifSIsInNlc3Npb25JbmRleCI6NH0seyJrZXkiOiJ0b2tlbiIsInZhbHVlIjoiIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImFueSIsInNlc3Npb25WYWx1ZSI6IiIsInNlc3Npb25JbmRleCI6NX0seyJrZXkiOiJsb2NhbFRva2VuIiwidmFsdWUiOiIiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiYW55Iiwic2Vzc2lvblZhbHVlIjoiIiwic2Vzc2lvbkluZGV4Ijo2fV0=)

#### 6 - /files GET

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/16367637-84c8186c-37da-430c-b03d-47fe016f26ed?action=collection%2Ffork&collection-url=entityId%3D16367637-84c8186c-37da-430c-b03d-47fe016f26ed%26entityType%3Dcollection%26workspaceId%3D5364826e-9d9b-40a6-bcb6-3976c612ccce#?env%5BDocker%5D=W3sia2V5IjoiUE9SVCIsInZhbHVlIjoiNjAwMCIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJkZWZhdWx0Iiwic2Vzc2lvblZhbHVlIjoiNjAwMCIsInNlc3Npb25JbmRleCI6MH0seyJrZXkiOiJVUkwiLCJ2YWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiZGVmYXVsdCIsInNlc3Npb25WYWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJzZXNzaW9uSW5kZXgiOjF9LHsia2V5IjoidmFsaWRfdXNlcm5hbWUiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjJ9LHsia2V5IjoidmFsaWRfcGFzc3dvcmQiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjN9LHsia2V5IjoicmVxdWVzdEJvZHkiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiJ7XCJ1c2VybmFtZVwiOlwiYWxvbnNvXCIsXCJlbWFpbFwiOlwiYS5jYW50dUB1bmlhbmRlcy5lZHUuY29cIixcInBhc3N3b3JkX2NvbmZpcm1hdGlvblwiOlwiMSMyM2w0RlwifSIsInNlc3Npb25JbmRleCI6NH0seyJrZXkiOiJ0b2tlbiIsInZhbHVlIjoiIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImFueSIsInNlc3Npb25WYWx1ZSI6IiIsInNlc3Npb25JbmRleCI6NX0seyJrZXkiOiJsb2NhbFRva2VuIiwidmFsdWUiOiIiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiYW55Iiwic2Vzc2lvblZhbHVlIjoiIiwic2Vzc2lvbkluZGV4Ijo2fV0=)

#### 7 - /mail/send

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/16367637-ba57b3a9-b9b5-4bca-83c8-0ab7a44b8477?action=collection%2Ffork&collection-url=entityId%3D16367637-ba57b3a9-b9b5-4bca-83c8-0ab7a44b8477%26entityType%3Dcollection%26workspaceId%3D5364826e-9d9b-40a6-bcb6-3976c612ccce#?env%5BDocker%5D=W3sia2V5IjoiUE9SVCIsInZhbHVlIjoiNjAwMCIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJkZWZhdWx0Iiwic2Vzc2lvblZhbHVlIjoiNjAwMCIsInNlc3Npb25JbmRleCI6MH0seyJrZXkiOiJVUkwiLCJ2YWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiZGVmYXVsdCIsInNlc3Npb25WYWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJzZXNzaW9uSW5kZXgiOjF9LHsia2V5IjoidmFsaWRfdXNlcm5hbWUiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjJ9LHsia2V5IjoidmFsaWRfcGFzc3dvcmQiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjN9LHsia2V5IjoicmVxdWVzdEJvZHkiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiJ7XCJ1c2VybmFtZVwiOlwiYWxvbnNvXCIsXCJlbWFpbFwiOlwiYS5jYW50dUB1bmlhbmRlcy5lZHUuY29cIixcInBhc3N3b3JkX2NvbmZpcm1hdGlvblwiOlwiMSMyM2w0RlwifSIsInNlc3Npb25JbmRleCI6NH0seyJrZXkiOiJ0b2tlbiIsInZhbHVlIjoiIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImFueSIsInNlc3Npb25WYWx1ZSI6IiIsInNlc3Npb25JbmRleCI6NX0seyJrZXkiOiJsb2NhbFRva2VuIiwidmFsdWUiOiIiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiYW55Iiwic2Vzc2lvblZhbHVlIjoiIiwic2Vzc2lvbkluZGV4Ijo2fV0=)

#### 8 - /tasks DELETE

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/16367637-e920f4cd-34df-4318-b70e-a359dffdabe4?action=collection%2Ffork&collection-url=entityId%3D16367637-e920f4cd-34df-4318-b70e-a359dffdabe4%26entityType%3Dcollection%26workspaceId%3D5364826e-9d9b-40a6-bcb6-3976c612ccce#?env%5BDocker%5D=W3sia2V5IjoiUE9SVCIsInZhbHVlIjoiNjAwMCIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJkZWZhdWx0Iiwic2Vzc2lvblZhbHVlIjoiNjAwMCIsInNlc3Npb25JbmRleCI6MH0seyJrZXkiOiJVUkwiLCJ2YWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiZGVmYXVsdCIsInNlc3Npb25WYWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJzZXNzaW9uSW5kZXgiOjF9LHsia2V5IjoidmFsaWRfdXNlcm5hbWUiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjJ9LHsia2V5IjoidmFsaWRfcGFzc3dvcmQiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjN9LHsia2V5IjoicmVxdWVzdEJvZHkiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiJ7XCJ1c2VybmFtZVwiOlwiYWxvbnNvXCIsXCJlbWFpbFwiOlwiYS5jYW50dUB1bmlhbmRlcy5lZHUuY29cIixcInBhc3N3b3JkX2NvbmZpcm1hdGlvblwiOlwiMSMyM2w0RlwifSIsInNlc3Npb25JbmRleCI6NH0seyJrZXkiOiJ0b2tlbiIsInZhbHVlIjoiIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImFueSIsInNlc3Npb25WYWx1ZSI6IiIsInNlc3Npb25JbmRleCI6NX0seyJrZXkiOiJsb2NhbFRva2VuIiwidmFsdWUiOiIiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiYW55Iiwic2Vzc2lvblZhbHVlIjoiIiwic2Vzc2lvbkluZGV4Ijo2fV0=)

## Evidencia del experimento - Entrega 1

### Video de presentación del proyecto y resultados obtenidos

https://user-images.githubusercontent.com/60992168/197699442-23ed543f-9090-4360-86d1-5e3decbd90a8.mp4

### Video paso a paso de reproducción del experimento

https://user-images.githubusercontent.com/60992168/197675090-523880f7-7e58-440d-981f-485d6432b4da.mp4

### Paso a paso de reproducción del experimento

Para la ejecución correcta de los siguientes pasos, se espera que usted como usuario tenga instaladas las herramientas
necesarias en su máquina local: git, Docker, Postman. Así mismo se espera que tenga conocimientos de uso de la terminal.

1. Clonar el repositorio con el comando:

   ```shell
   git clone https://github.com/lmaero/MISW4204-CloudConversionTool.git
   ```
   <br/>
2. Navegar al directorio clonado
   ```shell
   cd MISW4204-CloudConversionTool
   ```
   <br/>
3. Verifique que los puertos 5050, 5432, 6000, 6379, 6500 y 7000 de su máquina local no se encuentran en uso, estos
   puertos serán usados por Docker para ejecutar los contenedores que exponen los servicios de la aplicación:

    - Postgres como base de datos (5432)
    - gunicorn como servidor multithread para la aplicación desarrollada en Flask (6000)
    - nginx como servidor web sirviendo la aplicación expuesta por gunicorn (6500)
    - pgadmin como gestor gráfico de la base de datos en caso de querer verificar las transacciones y datos
      almacenados (5050)
    - redis como broker para la cola de mensajería implementada con Celery (6379)
    - y por último un MailNotificator implementado como una aplicación en Flask. (7000)

   <br/>
4. Abra una instancia de la terminal o consola de comandos y ejecute el siguiente comando, éste creará y ejecutará los
   contenedores necesarios para continuar con la ejecución de las pruebas planteadas en Postman.
   ```shell
   docker compose up -d --force-recreate
   ```
   Permita que los contenedores inicien sus servicios, este proceso tardará aproximadamente 1 minuto, pero dependerá de
   varios factores como la velocidad de su conexión de internet y las características de rendimiento de su máquina
   local.
   <br/>
   <br/>

5. En este punto todos los servicios estarán disponibles y puede continuar la ejecución de las pruebas de Postman,
   relacionadas a continuación. Si tiene Docker Desktop instalado, puede verificar el estado de los servicios tal como
   se muestra en la imagen a continuación:

   ![Screenshot from 2022-10-24 20-58-04](https://user-images.githubusercontent.com/60992168/197670599-a2505ca3-6e28-4616-8181-3339671771d5.png)
   <br/>
   <br/>
   **Nota:** En caso que desee repetir las pruebas recuerde reiniciar los contenedores, eliminándolos con el comando a
   continuación y repitiendo el comando del paso 4.

   ```shell
   docker compose down -v
   ```

## Ejecución de solicitudes - Postman

**Nota:** los escenarios están planteados para ser ejecutados una sola vez y en el orden planteado.

### Workspace de Postman - Público

[Postman Workspace](https://www.postman.com/lmaero-pro/workspace/misw4204-conversiontool)

### Colecciones de Postman comprimidas

Los botones a continuación le permiten hacer fork de las colecciones para ejecutarlas con el runner de Postman. Si
prefiere importarlas, dispusimos de un vínculo en la Wiki del repositorio, que contiene un archivo comprimido con las
colecciones, puede descargarlo en la siguiente sección:

[Ir a archivo comprimido en la Wiki](https://github.com/lmaero/MISW4204-CloudConversionTool/wiki/Documentaci%C3%B3n-para-Usuarios#colecciones-de-postman)

Así mismo, en caso de que no desee ejecutarlas, puede verificar los resultados de la ejecución en el siguiente vínculo:
[Ir a escenarios de prueba ejecutados](https://github.com/lmaero/MISW4204-CloudConversionTool/wiki/Documentaci%C3%B3n-para-Usuarios#pruebas-api-postman)

### Colecciones para el Postman runner

#### 1 - /auth/signup

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/16367637-8e371886-137d-40fd-9ea8-0180a7108975?action=collection%2Ffork&collection-url=entityId%3D16367637-8e371886-137d-40fd-9ea8-0180a7108975%26entityType%3Dcollection%26workspaceId%3D5364826e-9d9b-40a6-bcb6-3976c612ccce#?env%5BDocker%5D=W3sia2V5IjoiUE9SVCIsInZhbHVlIjoiNjAwMCIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJkZWZhdWx0Iiwic2Vzc2lvblZhbHVlIjoiNjAwMCIsInNlc3Npb25JbmRleCI6MH0seyJrZXkiOiJVUkwiLCJ2YWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiZGVmYXVsdCIsInNlc3Npb25WYWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJzZXNzaW9uSW5kZXgiOjF9LHsia2V5IjoidmFsaWRfdXNlcm5hbWUiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjJ9LHsia2V5IjoidmFsaWRfcGFzc3dvcmQiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjN9LHsia2V5IjoicmVxdWVzdEJvZHkiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiJ7XCJ1c2VybmFtZVwiOlwiYWxvbnNvXCIsXCJlbWFpbFwiOlwiYS5jYW50dUB1bmlhbmRlcy5lZHUuY29cIixcInBhc3N3b3JkX2NvbmZpcm1hdGlvblwiOlwiMSMyM2w0RlwifSIsInNlc3Npb25JbmRleCI6NH0seyJrZXkiOiJ0b2tlbiIsInZhbHVlIjoiIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImFueSIsInNlc3Npb25WYWx1ZSI6IiIsInNlc3Npb25JbmRleCI6NX0seyJrZXkiOiJsb2NhbFRva2VuIiwidmFsdWUiOiIiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiYW55Iiwic2Vzc2lvblZhbHVlIjoiIiwic2Vzc2lvbkluZGV4Ijo2fV0=)

#### 2 - /auth/login

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/16367637-9de5e6fa-383a-4c06-a8d7-0124cde6a9b0?action=collection%2Ffork&collection-url=entityId%3D16367637-9de5e6fa-383a-4c06-a8d7-0124cde6a9b0%26entityType%3Dcollection%26workspaceId%3D5364826e-9d9b-40a6-bcb6-3976c612ccce#?env%5BDocker%5D=W3sia2V5IjoiUE9SVCIsInZhbHVlIjoiNjAwMCIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJkZWZhdWx0Iiwic2Vzc2lvblZhbHVlIjoiNjAwMCIsInNlc3Npb25JbmRleCI6MH0seyJrZXkiOiJVUkwiLCJ2YWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiZGVmYXVsdCIsInNlc3Npb25WYWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJzZXNzaW9uSW5kZXgiOjF9LHsia2V5IjoidmFsaWRfdXNlcm5hbWUiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjJ9LHsia2V5IjoidmFsaWRfcGFzc3dvcmQiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjN9LHsia2V5IjoicmVxdWVzdEJvZHkiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiJ7XCJ1c2VybmFtZVwiOlwiYWxvbnNvXCIsXCJlbWFpbFwiOlwiYS5jYW50dUB1bmlhbmRlcy5lZHUuY29cIixcInBhc3N3b3JkX2NvbmZpcm1hdGlvblwiOlwiMSMyM2w0RlwifSIsInNlc3Npb25JbmRleCI6NH0seyJrZXkiOiJ0b2tlbiIsInZhbHVlIjoiIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImFueSIsInNlc3Npb25WYWx1ZSI6IiIsInNlc3Npb25JbmRleCI6NX0seyJrZXkiOiJsb2NhbFRva2VuIiwidmFsdWUiOiIiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiYW55Iiwic2Vzc2lvblZhbHVlIjoiIiwic2Vzc2lvbkluZGV4Ijo2fV0=)

#### 3 - /tasks - POST

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/16367637-72352066-c2f8-42b4-849c-409c969e853b?action=collection%2Ffork&collection-url=entityId%3D16367637-72352066-c2f8-42b4-849c-409c969e853b%26entityType%3Dcollection%26workspaceId%3D5364826e-9d9b-40a6-bcb6-3976c612ccce#?env%5BDocker%5D=W3sia2V5IjoiUE9SVCIsInZhbHVlIjoiNjAwMCIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJkZWZhdWx0Iiwic2Vzc2lvblZhbHVlIjoiNjAwMCIsInNlc3Npb25JbmRleCI6MH0seyJrZXkiOiJVUkwiLCJ2YWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiZGVmYXVsdCIsInNlc3Npb25WYWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJzZXNzaW9uSW5kZXgiOjF9LHsia2V5IjoidmFsaWRfdXNlcm5hbWUiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjJ9LHsia2V5IjoidmFsaWRfcGFzc3dvcmQiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjN9LHsia2V5IjoicmVxdWVzdEJvZHkiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiJ7XCJ1c2VybmFtZVwiOlwiYWxvbnNvXCIsXCJlbWFpbFwiOlwiYS5jYW50dUB1bmlhbmRlcy5lZHUuY29cIixcInBhc3N3b3JkX2NvbmZpcm1hdGlvblwiOlwiMSMyM2w0RlwifSIsInNlc3Npb25JbmRleCI6NH0seyJrZXkiOiJ0b2tlbiIsInZhbHVlIjoiIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImFueSIsInNlc3Npb25WYWx1ZSI6IiIsInNlc3Npb25JbmRleCI6NX0seyJrZXkiOiJsb2NhbFRva2VuIiwidmFsdWUiOiIiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiYW55Iiwic2Vzc2lvblZhbHVlIjoiIiwic2Vzc2lvbkluZGV4Ijo2fV0=)

#### 4 - /tasks - GET

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/16367637-071a172c-d9d0-4d43-873e-cde499236216?action=collection%2Ffork&collection-url=entityId%3D16367637-071a172c-d9d0-4d43-873e-cde499236216%26entityType%3Dcollection%26workspaceId%3D5364826e-9d9b-40a6-bcb6-3976c612ccce#?env%5BDocker%5D=W3sia2V5IjoiUE9SVCIsInZhbHVlIjoiNjAwMCIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJkZWZhdWx0Iiwic2Vzc2lvblZhbHVlIjoiNjAwMCIsInNlc3Npb25JbmRleCI6MH0seyJrZXkiOiJVUkwiLCJ2YWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiZGVmYXVsdCIsInNlc3Npb25WYWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJzZXNzaW9uSW5kZXgiOjF9LHsia2V5IjoidmFsaWRfdXNlcm5hbWUiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjJ9LHsia2V5IjoidmFsaWRfcGFzc3dvcmQiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjN9LHsia2V5IjoicmVxdWVzdEJvZHkiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiJ7XCJ1c2VybmFtZVwiOlwiYWxvbnNvXCIsXCJlbWFpbFwiOlwiYS5jYW50dUB1bmlhbmRlcy5lZHUuY29cIixcInBhc3N3b3JkX2NvbmZpcm1hdGlvblwiOlwiMSMyM2w0RlwifSIsInNlc3Npb25JbmRleCI6NH0seyJrZXkiOiJ0b2tlbiIsInZhbHVlIjoiIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImFueSIsInNlc3Npb25WYWx1ZSI6IiIsInNlc3Npb25JbmRleCI6NX0seyJrZXkiOiJsb2NhbFRva2VuIiwidmFsdWUiOiIiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiYW55Iiwic2Vzc2lvblZhbHVlIjoiIiwic2Vzc2lvbkluZGV4Ijo2fV0=)

#### 5 - /tasks PUT

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/16367637-be8674c3-abcd-488e-985f-51a3a05568d1?action=collection%2Ffork&collection-url=entityId%3D16367637-be8674c3-abcd-488e-985f-51a3a05568d1%26entityType%3Dcollection%26workspaceId%3D5364826e-9d9b-40a6-bcb6-3976c612ccce#?env%5BDocker%5D=W3sia2V5IjoiUE9SVCIsInZhbHVlIjoiNjAwMCIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJkZWZhdWx0Iiwic2Vzc2lvblZhbHVlIjoiNjAwMCIsInNlc3Npb25JbmRleCI6MH0seyJrZXkiOiJVUkwiLCJ2YWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiZGVmYXVsdCIsInNlc3Npb25WYWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJzZXNzaW9uSW5kZXgiOjF9LHsia2V5IjoidmFsaWRfdXNlcm5hbWUiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjJ9LHsia2V5IjoidmFsaWRfcGFzc3dvcmQiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjN9LHsia2V5IjoicmVxdWVzdEJvZHkiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiJ7XCJ1c2VybmFtZVwiOlwiYWxvbnNvXCIsXCJlbWFpbFwiOlwiYS5jYW50dUB1bmlhbmRlcy5lZHUuY29cIixcInBhc3N3b3JkX2NvbmZpcm1hdGlvblwiOlwiMSMyM2w0RlwifSIsInNlc3Npb25JbmRleCI6NH0seyJrZXkiOiJ0b2tlbiIsInZhbHVlIjoiIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImFueSIsInNlc3Npb25WYWx1ZSI6IiIsInNlc3Npb25JbmRleCI6NX0seyJrZXkiOiJsb2NhbFRva2VuIiwidmFsdWUiOiIiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiYW55Iiwic2Vzc2lvblZhbHVlIjoiIiwic2Vzc2lvbkluZGV4Ijo2fV0=)

#### 6 - /files GET

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/16367637-84c8186c-37da-430c-b03d-47fe016f26ed?action=collection%2Ffork&collection-url=entityId%3D16367637-84c8186c-37da-430c-b03d-47fe016f26ed%26entityType%3Dcollection%26workspaceId%3D5364826e-9d9b-40a6-bcb6-3976c612ccce#?env%5BDocker%5D=W3sia2V5IjoiUE9SVCIsInZhbHVlIjoiNjAwMCIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJkZWZhdWx0Iiwic2Vzc2lvblZhbHVlIjoiNjAwMCIsInNlc3Npb25JbmRleCI6MH0seyJrZXkiOiJVUkwiLCJ2YWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiZGVmYXVsdCIsInNlc3Npb25WYWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJzZXNzaW9uSW5kZXgiOjF9LHsia2V5IjoidmFsaWRfdXNlcm5hbWUiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjJ9LHsia2V5IjoidmFsaWRfcGFzc3dvcmQiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjN9LHsia2V5IjoicmVxdWVzdEJvZHkiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiJ7XCJ1c2VybmFtZVwiOlwiYWxvbnNvXCIsXCJlbWFpbFwiOlwiYS5jYW50dUB1bmlhbmRlcy5lZHUuY29cIixcInBhc3N3b3JkX2NvbmZpcm1hdGlvblwiOlwiMSMyM2w0RlwifSIsInNlc3Npb25JbmRleCI6NH0seyJrZXkiOiJ0b2tlbiIsInZhbHVlIjoiIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImFueSIsInNlc3Npb25WYWx1ZSI6IiIsInNlc3Npb25JbmRleCI6NX0seyJrZXkiOiJsb2NhbFRva2VuIiwidmFsdWUiOiIiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiYW55Iiwic2Vzc2lvblZhbHVlIjoiIiwic2Vzc2lvbkluZGV4Ijo2fV0=)

#### 7 - /mail/send

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/16367637-ba57b3a9-b9b5-4bca-83c8-0ab7a44b8477?action=collection%2Ffork&collection-url=entityId%3D16367637-ba57b3a9-b9b5-4bca-83c8-0ab7a44b8477%26entityType%3Dcollection%26workspaceId%3D5364826e-9d9b-40a6-bcb6-3976c612ccce#?env%5BDocker%5D=W3sia2V5IjoiUE9SVCIsInZhbHVlIjoiNjAwMCIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJkZWZhdWx0Iiwic2Vzc2lvblZhbHVlIjoiNjAwMCIsInNlc3Npb25JbmRleCI6MH0seyJrZXkiOiJVUkwiLCJ2YWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiZGVmYXVsdCIsInNlc3Npb25WYWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJzZXNzaW9uSW5kZXgiOjF9LHsia2V5IjoidmFsaWRfdXNlcm5hbWUiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjJ9LHsia2V5IjoidmFsaWRfcGFzc3dvcmQiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjN9LHsia2V5IjoicmVxdWVzdEJvZHkiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiJ7XCJ1c2VybmFtZVwiOlwiYWxvbnNvXCIsXCJlbWFpbFwiOlwiYS5jYW50dUB1bmlhbmRlcy5lZHUuY29cIixcInBhc3N3b3JkX2NvbmZpcm1hdGlvblwiOlwiMSMyM2w0RlwifSIsInNlc3Npb25JbmRleCI6NH0seyJrZXkiOiJ0b2tlbiIsInZhbHVlIjoiIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImFueSIsInNlc3Npb25WYWx1ZSI6IiIsInNlc3Npb25JbmRleCI6NX0seyJrZXkiOiJsb2NhbFRva2VuIiwidmFsdWUiOiIiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiYW55Iiwic2Vzc2lvblZhbHVlIjoiIiwic2Vzc2lvbkluZGV4Ijo2fV0=)

#### 8 - /tasks DELETE

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/16367637-e920f4cd-34df-4318-b70e-a359dffdabe4?action=collection%2Ffork&collection-url=entityId%3D16367637-e920f4cd-34df-4318-b70e-a359dffdabe4%26entityType%3Dcollection%26workspaceId%3D5364826e-9d9b-40a6-bcb6-3976c612ccce#?env%5BDocker%5D=W3sia2V5IjoiUE9SVCIsInZhbHVlIjoiNjAwMCIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJkZWZhdWx0Iiwic2Vzc2lvblZhbHVlIjoiNjAwMCIsInNlc3Npb25JbmRleCI6MH0seyJrZXkiOiJVUkwiLCJ2YWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiZGVmYXVsdCIsInNlc3Npb25WYWx1ZSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjAwMC9hcGkiLCJzZXNzaW9uSW5kZXgiOjF9LHsia2V5IjoidmFsaWRfdXNlcm5hbWUiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjJ9LHsia2V5IjoidmFsaWRfcGFzc3dvcmQiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjN9LHsia2V5IjoicmVxdWVzdEJvZHkiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiJ7XCJ1c2VybmFtZVwiOlwiYWxvbnNvXCIsXCJlbWFpbFwiOlwiYS5jYW50dUB1bmlhbmRlcy5lZHUuY29cIixcInBhc3N3b3JkX2NvbmZpcm1hdGlvblwiOlwiMSMyM2w0RlwifSIsInNlc3Npb25JbmRleCI6NH0seyJrZXkiOiJ0b2tlbiIsInZhbHVlIjoiIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImFueSIsInNlc3Npb25WYWx1ZSI6IiIsInNlc3Npb25JbmRleCI6NX0seyJrZXkiOiJsb2NhbFRva2VuIiwidmFsdWUiOiIiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiYW55Iiwic2Vzc2lvblZhbHVlIjoiIiwic2Vzc2lvbkluZGV4Ijo2fV0=)
