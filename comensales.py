import threading
import time
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

semaComensal = threading.Semaphore(1)
semaCocinero = threading.Semaphore(0)

class Cocinero(threading.Thread):
  def __init__(self):
    super().__init__()
    self.name = 'Cocinero'

  def run(self):
    global platosDisponibles
    
    while (True):
      semaCocinero.acquire()
      try:
        logging.info('Reponiendo los platos...')
        platosDisponibles = 3
      finally:
        semaComensal.release()

class Comensal(threading.Thread):
  def __init__(self, numero):
    super().__init__()
    self.name = f'Comensal {numero}'

  def run(self):
    global platosDisponibles
    
    semaComensal.acquire()
    try:
      if platosDisponibles == 0:
        semaCocinero.release()
        semaComensal.acquire()
      self.comer()
    finally:
      semaComensal.release()
    
  def comer(self):
    global platosDisponibles
    platosDisponibles -= 1
    logging.info(f'¡Qué rico! Quedan {platosDisponibles} platos')

platosDisponibles = 3
cantidadDeComensales = 20
Cocinero().start()


for i in range(cantidadDeComensales):
  Comensal(i).start()

