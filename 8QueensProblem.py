from random import randint
import time
 
N = 8
randomRestartCounter = 0;
changeCounter = 0;
 
#2 boyutlu bir satranç tahtası üzerinde rastgele bir state oluşturulur
def configureRandomly(board, state):
 
    # Iterating through the
    # column indices
    for i in range(N):
 
        #Vezirin kaçıncı satıra yerleştirileceğini bulmak için tam sayı bir index rastgele alınır
        state[i] = randint(0, 100000) % N;
        #Rastgele alınan satırın i. elemanına vezir yerleştirilir
        board[state[i]][i] = 1;
    
#2 boyutlu bir array olan satranç tahtasını yazdırmak için kullanılan fonksiyon
def printBoard(board):
     
    for i in range(N):
        print(*board[i])
 
# Satranç tahtasındaki vezirlerin kaçıncı satırın (elemanın değeri) hangi sütununa (index) konulduğunu gösteren durumu yazdırır
def printState( state):
    print(*state)
     
#İki state'in birbirinin aynısı olup olmadığını anlamamıza yarayan fonksiyon
def compareStates(state1, state2):
 
    for i in range(N):
        if (state1[i] != state2[i]):
            return False;
     
    return True;
 
# Oluşturulan tahtanın tüm kutularına aynı değeri verir
def fill(board, value):
     
    for i in range(N):
        for j in range(N):
            board[i][j] = value;
         
# Vezirlerin yerleştirilmiş olduğu bir satranç tahtasında kaç çift taşın birbirini yediği hesaplanır
def calculateObjective( board, state):
 
    #Bir satranç tahtasındaki vezirlerin saldırı patikasının üzerinde kaç tane taş olduğunu sayan sayaç
    attacking = 0;
 
    # For döngüsü ile satranç tahtasının üzerinde taş olan kareleri dolaşılır
    for i in range(N):
 
        # Her state[i]'nci satırda vezir, i'nci sütuna yerleştirilir.
 
        # Taşın solunda herhangi bir taş olup olmadığını kontrol etmek için satır aynı tutulur, sütun indeksi 0 oluncaya yada bir taşla karşılaşılıncaya kadar bir azaltılır
        row = state[i]
        col = i - 1;
        while (col >= 0 and board[row][col] != 1) :
            col -= 1
         
        #Bir taşla karşılaşıldığında sayaç bir arttırılır
        if (col >= 0 and board[row][col] == 1) :
            attacking += 1;
         
        # Taşın sağında herhangi bir taş olup olmadığını kontrol etmek için satır aynı tutulur, sütun indeksi "eleman sayısı - 1" oluncaya yada bir taşla karşılaşılıncaya kadar bir arttırılır
        row = state[i]
        col = i + 1;
        while (col < N and board[row][col] != 1):
            col += 1;
        #Bir taşla karşılaşıldığında sayaç bir arttırılır
        if (col < N and board[row][col] == 1) :
            attacking += 1;
         
        # Taşın sol üst çaprazında herhangi bir taş olup olmadığını kontrol etmek için satır da sütun da 0 oluncaya yada bir taşla karşılaşılıncaya kadar bir azaltılır
        row = state[i] - 1
        col = i - 1;
        while (col >= 0 and row >= 0 and board[row][col] != 1) :
            col-= 1;
            row-= 1;
        #Bir taşla karşılaşıldığında sayaç bir arttırılır
        if (col >= 0 and row >= 0  and board[row][col] == 1) :
            attacking+= 1;
         
        # Taşın sağ alt çaprazında herhangi bir taş olup olmadığını kontrol etmek için satır da sütun da "eleman sayısı - 1" oluncaya yada bir taşla karşılaşılıncaya kadar bir arttırılır
        row = state[i] + 1
        col = i + 1;
        while (col < N and row < N  and board[row][col] != 1) :
            col+= 1;
            row+= 1;
        #Bir taşla karşılaşıldığında sayaç bir arttırılır
        if (col < N and row < N and board[row][col] == 1) :
            attacking += 1;
         
        # Taşın sol alt çaprazında herhangi bir taş olup olmadığını kontrol etmek için satır bir arttırılır, sütun bir eksiltilir
        row = state[i] + 1
        col = i - 1;
        while (col >= 0 and row < N  and board[row][col] != 1) :
            col -= 1;
            row += 1;
        #Bir taşla karşılaşıldığında sayaç bir arttırılır
        if (col >= 0 and row < N and board[row][col] == 1) :
            attacking += 1;
         
        # Taşın sağ üst çaprazında herhangi bir taş olup olmadığını kontrol etmek için satır bir azaltılır, sütun bir arttırılır
        row = state[i] - 1
        col = i + 1;
        while (col < N and row >= 0  and board[row][col] != 1) :
            col += 1;
            row -= 1;
        #Bir taşla karşılaşıldığında sayaç bir arttırılır 
        if (col < N and row >= 0 and board[row][col] == 1) :
            attacking += 1;
         
    # Bir taş başka bir taş ile kesiştiğinde diğer taş da mevcut taşla kesiceği için aynı kesişimleri iki kez almamak için sonuç ikiye bölünür
    return int(attacking / 2);
 
# Durumu verilmiş bir satranç tahtasını oluşturulmak için kullanılan fonksiyon
def generateBoard( board, state):
    fill(board, 0);
    for i in range(N):
        board[state[i]][i] = 1;
     
# Bir durumu başka bir duruma kopyalayan fonksiyon
def copyState( state1, state2):
 
    for i in range(N):
        state1[i] = state2[i];
     
# Bir durumdan sonra gelen komşu durumu hesaplayan fonksiyon
def getNeighbour(board, state):

    # Elde edebileceğimiz en iyi komşuu elde etmek istediğimiz için optimal state ve optimal board oluşturulur
    opBoard = [[0 for _ in range(N)] for _ in range(N)]
    opState = [0 for _ in range(N)]
 
    #Optimal state'e ve optimal board'a mevcut durum ve mevcut board kopyalanır
    copyState(opState, state);
    generateBoard(opBoard, opState);
 
    #Mevcut boardın değeri hesaplanır
    opObjective  = calculateObjective(opBoard, opState);
 
    # Komşu durum ve komşu board oluşturulur
    NeighbourBoard = [[0 for _ in range(N)] for _ in range(N)]
    NeighbourState = [0 for _ in range(N)]

    #Bir soraki gelecek olan durum ve board, mevcut durum ve board üzerinden hesaplanılacağı için mevcut durum ve board komşu durum ve board'a kopyalanır.
    copyState(NeighbourState, state);
    generateBoard(NeighbourBoard, NeighbourState);
 
    # Mevcut board'ın tüm kareleri üzerinde deneme yanılma yoluyla testler yaparak daha optimal bir durum/board bulunması hedeflenir
    for i in range(N):
        for j in range(N):
            
            # Eğer mevcut board'da taşın konulduğu yer ile döngüde üzerinde dolaştığımız kare aynı değil ise
            if (j != state[i]) :
                
                #Taşın mevcut konumu yeni konum ile değiştirilir
                NeighbourState[i] = j;
                NeighbourBoard[NeighbourState[i]][i] = 1;
                NeighbourBoard[state[i]][i] = 0;
 
                # Yeni oluşan board'un (komşunun) değeri hesaplanır
                temp = calculateObjective( NeighbourBoard, NeighbourState);
 
                
                #Eğer komşu durumda birbirini yiyen taş sayısı daha az ise yeni optimal durum komşu durum olur
                if (temp < opObjective) :
                    opObjective = temp;
                    copyState(opState, NeighbourState);
                    generateBoard(opBoard, opState);
                 
                # Yapılan değişiklik geri alınarak komşu durum mevcut duruma geri getirilir.Amaç bir adım uzakliktaki komşular içerisinden en iyisini bulmaktır.
                NeighbourBoard[NeighbourState[i]][i] = 0;
                NeighbourState[i] = state[i];
                NeighbourBoard[state[i]][i] = 1;
             
    # Optimal komşu durum,mevcut durum olarak ayarlanır
    copyState(state, opState);
    fill(board, 0);
    generateBoard(board, state);
 
def hillClimbing(board, state):
 
    global randomRestartCounter
    global changeCounter

    # Komşu board ve state oluşturulur
 
    neighbourBoard = [[0 for _ in range(N)] for _ in range(N)]
    neighbourState = [0 for _ in range(N)]
 
    copyState(neighbourState, state);
    generateBoard(neighbourBoard, neighbourState);

    print("-----------------------------------------------")
    printBoard(board);
     
    while True:
        
        #Optimal komşu, mevcut state üzerinden elde edileceği için komşu board ve state'e mevcut state ve board kopyalanır
        copyState(state, neighbourState);
        generateBoard(board, state);
 
        # Optimal komşu elde edilir
 
        getNeighbour(neighbourBoard, neighbourState);

        #Eğer komşu durum ile mevcut durum birbirinin aynısı ise bu mevcut durumdan daha optimal bir durum olmadığı yani bir çukurda(değeri en düşük state'i aradığımız için) olduğumuz anlamına gelir.
        if (compareStates(state, neighbourState)) :
            
            if(calculateObjective(board,state) == 0) :#Eğer state'in değeri 0 ise bu optimal değeri bulduğumuz anlamına gelir
                printBoard(board);
                break;
            else:#Eğer state'in değeri 0 değil ise local minimumda sıkışıldığı anlamına gelir ve random restart yapılır
                configureRandomly(neighbourBoard,neighbourState);
                changeCounter += calculateDifference(board,neighbourBoard);
                randomRestartCounter +=1
                print("RANDOM RESTART YAPILDI");
         #Eğer komşu durum ile mevcut durumdan birbirinden farklı ama değerleri aynı ise bu bir plato/shoulder üzerindedir.Random restart yapılır
        elif (calculateObjective(board, state) == calculateObjective( neighbourBoard,neighbourState)):

            configureRandomly(neighbourBoard,neighbourState);
            changeCounter += calculateDifference(board,neighbourBoard);
            randomRestartCounter += 1;
            print("RANDOM RESTART YAPILDI");
        
        else:#Mevcut durum ile komşu durum birbirinden farklıdır ve komşu durum daha optimaldir.Bir sonraki döngünün başında mevcut durum şuanki komşu durum olarak ayarlanır
            changeCounter += 1;

        print("--------------------------------------------")
        printBoard(neighbourBoard);
        print("--------------------------------------------")

#İki board'ın birbiriyle aynı olup olmadığı anlaşılır
def calculateDifference(board,newBoard):
    difference = 0;
    for i in range(N):

        for j in range(N):

            if(board[i][j]!=newBoard[i][j]):
                
                difference += 1;

    return int(difference/2);

#8 Queens probleminin ne kadar sürede çözüleceğini bulmak için başlatılma zamanı alınır.
startTime = time.time()

#Bir board ve state oluşturulur
state = [0] * N
board = [[0 for _ in range(N)] for _ in range(N)]

# Oluşturulan state ve board'dan rastgele bir başlangıç durumu ve board'ı elde edilir
configureRandomly(board, state);
 
# Hill climbing ile problem çözdürülür
hillClimbing(board, state);
#Executionun sonlanma zamanı alınır
endTime = time.time()
#Sonlanma zamanından başlama zamanı çıkartılarak execution süresi bulunur
duration = endTime - startTime;

print("SÜRE")
print(duration)
print("-------------------------------------------------------")
print("RANDOM RESTART SAYISI")
print(randomRestartCounter)
print("-------------------------------------------------------")
print("YAPILAN HAMLE SAYISI")
print(changeCounter)
print("-------------------------------------------------------")