import threading
import time
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

semaphore = threading.Semaphore(3)

class Cocinero(threading.Thread):
  def __init__(self):
    super().__init__()
    self.name = 'Cocinero'

  def run(self):
    global platosDisponibles
    semaphore.release()
    while (True):
      logging.info('Reponiendo los platos...')
      platosDisponibles = 3

class Comensal(threading.Thread):
  def __init__(self, numero):
    super().__init__()
    self.name = f'Comensal {numero}'

  def run(self):
    global platosDisponibles
    global semaphore
    semaphore.acquire()
    platosDisponibles -= 1
    logging.info(f'¡Qué rico! Quedan {platosDisponibles} platos')

platosDisponibles = 3
cantidadDeComensales = 5
Cocinero().start()


for i in range(cantidadDeComensales):
  Comensal(i).start()

