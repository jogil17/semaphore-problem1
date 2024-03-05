import time
import threading

NUM_RONDAS    = 3
NUM_ESTUDIANTES  = int(input("Inserte el número total de estudiantes: "))  
MAX_FIESTA    = int(input("Inserte el número máximo de estudiantes para hacer fiesta: "))

#semáforos
sem_estudiante = threading.Semaphore(0)
sem_director  = threading.Semaphore(0)
mutex       = threading.Semaphore(1)

#variables
enLaSala    = 0
n_estudiantes    = NUM_ESTUDIANTES #para saber el número de estudiantes que queda por abandonar la sala

# Estados del director
FUERA        = 0
ESPERANDO    = 1
DENTRO       = 2
director     = FUERA  #inicialización del estado del director

nombres = [
        'Jogil','Manuel','Pedro','Manolo','Sara','Noelia','Gilda','Javier','Paco','Juan','Marisabel','Julio',
        'Sergio','Bryan','Jaden', 'Carmen','Kiko','Lola','Luisa','Sabrina','Sufi','Sufi','Pepito','Uriel'
    ] 

#función del director
def Director():

    global director
    global enLaSala
    
    #bucle con el número de rondas asignado
    for i in range(1, NUM_RONDAS + 1):
        
        time.sleep(0)
        
        mutex.acquire()

        print("     El Sr Director comienza la ronda")
        
        if (enLaSala == 0): #en caso de que en la sala no haya estudiantes

            print("     El Director ve que no hay nadie en la sala de estudios")
        
        elif (enLaSala < MAX_FIESTA): #en caso de que en la sala haya estudiantes pero no se ha montado una fiesta

            print("     El Director esta esperando para entrar. No molesta a los que estudian")
            director = ESPERANDO  #cambiamos el estado del director a esperando en la puerta
            
            mutex.release()
            sem_director.acquire()  #el director se queda esperando en la puerta
            
            if (enLaSala == 0):

                print("     El Director ve que no hay nadie en la sala de estudios")
            
            else:

                director = DENTRO  #el director entra en la sala para parar la fiesta

                print("     El Director está dentro de la sala de estudios: ¡SE HA ACABADO LA FIESTA!")
                sem_estudiante.release() #libera estudiantes para que abandonen la sala
                sem_director.acquire()  #el director se queda esperando a que todos hayan salido
        
        else:  #en caso de que haya fiesta

            print("     El Director está dentro de la sala de estudios: ¡SE HA ACABADO LA FIESTA!")
            director = DENTRO
            sem_estudiante.release()
            sem_director.acquire()


        print("     El Director acaba la ronda {} de {}" .format(i,NUM_RONDAS))
        director = FUERA  #Cuando el director acaba la ronda se va fuera de la sala

        mutex.release()
    
def Estudiante(nom):

    global director
    global enLaSala
    global n_estudiantes
    
    #THINK
    time.sleep(0)
    
    #ENTRANT
    mutex.acquire()

    enLaSala = enLaSala + 1  #un estudiante entra a la sala, incrementamos contador
    n_estudiantes = n_estudiantes - 1   #quedan x por entrar
    print("{} entra a la sala de estudios, número de estudiantes: {}".format(nom,enLaSala))
    
    if(enLaSala < MAX_FIESTA):  #en caso de que en la sala no haya fiesta
        print("{} estudia".format(nom))  #estudia
        mutex.release()
        
    else:  #en caso de que haya un número mayor de alumnos se monta una fiesta 
        print("{}: FIESTA!!!!!".format(nom))
        if(director == ESPERANDO):  #si el director está esperando en la puerta
            print("{}: CUIDADO que viene el director!!!!!".format(nom))
            sem_director.release()  #liberamos al director
        else:
            mutex.release()

    if(n_estudiantes == 0): 

        sem_estudiante.release()


    while(director != DENTRO and n_estudiantes != 0):
        pass

    sem_estudiante.acquire() 

    enLaSala = enLaSala - 1  #estudiante sale de la sala, ha terminado de estudiar
    print("{} sale de la sala de estudio, número de estudiantes: {}".format(nom, enLaSala))
    
    if (enLaSala != 0):
        sem_estudiante.release()
    
    elif (director == ESPERANDO): #si no había fiesta el último estudiante libera al director
        print("{}: ADIÓS Señor Director, puede entrar si quiere, no hay nadie".format(nom))
        sem_director.release()
    
    elif (director == DENTRO): #si había fiesta el último estudiante libera al director
        print("{}: ADIÓS Seór Director se queda solo".format(nom))
        sem_director.release()
    

def main():

    global MAX_FIESTA
    global NUM_ESTUDIANTES
    global nombres

    threads = []
    c = threading.Thread(target=Director)
    threads.append(c)

    for i in range(NUM_ESTUDIANTES):
        p = threading.Thread(target=Estudiante, args=(nombres[i],))
        threads.append(p)

    # Ejecutamos los hilos
    for t in threads:
        t.start()

    #Esperamos a que todos los hilos terminen
    for t in threads:
        t.join()

    print("SIMULACIÓN ACABADA")


if __name__ == "__main__":
    main()