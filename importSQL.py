import time
import os

tabSeparateur=[';','\t']
tabSeparateurEchape=[';','\\t']
#liste des types
tabPriorite=['STRING','DATE','FLOAT','BIGINT','INT']
tabType=[]
nbLigneALire=2000

def updateType(numCol,typeChg,val):
    typeAct=tabType[numCol][1]
    for hiveType in tabPriorite:
        if typeChg==hiveType:
            tabType[i][1]=typeChg
            tabType[i][2]=val
            return True
        if typeAct==hiveType:
            return True
    tabType[i][1]='STRING'
    tabType[i][2]='aucuneVAL'

def isFloat(string):
    try:
        float(string)
        return True
    except ValueError:
        a=0
    tmp=string[:]
    tmp=tmp.replace(',','.')
    try:
        float(tmp)
        return True
    except ValueError:
        return False
        

def isDate(string):
    isADate=1
    try:
        time.strptime(string, "%Y-%m-%d")
        return True
    except ValueError:
        a=0
    try:
        time.strptime(string, "%Y-%m-%d %T")
        return True
    except ValueError:
        return False

reqTot=[]
sepFichier=[]

for file in os.listdir():
    if file.endswith(".txt"):
        filename=file
    else :
        continue
    try:
        f = open(filename, 'r')
    except ValueError:
        print(ValueError)
        exit()
    print("\n\n********************************************************")
    print("traitement de "+file)
    print("********************************************************")
    colonnes=f.readline()
    i=-1
    tabColonnes=[0]
    while(len(tabColonnes)==1):
        i+=1
        tabColonnes=colonnes[:-1].split(tabSeparateur[i])
    separateurEchape=tabSeparateurEchape[i]
    separateur=tabSeparateur[i]
    sepFichier.append([file,separateur])
    tabType=[]
    for i in range(len(tabColonnes)):
        tabType.append([tabColonnes[i],'INT','NONE'])
    numLigne=0
    entrees=f.readline()
    while entrees!='':
        numLigne+=1
        """
        if(numLigne%100==0):
            print("\n"*50)
            print(str(int((100*numLigne)/nbLigneALire))+'%')
        """
        if(numLigne==nbLigneALire):
            break
        tabEntree=entrees[:-1].split(separateur)
        for i in range(len(tabEntree)):
            entree=tabEntree[i]
            isInt=False
            if(entree!=''):
                if(entree.isnumeric() or (entree[0]=='-' and entree[1:].isnumeric())):
                    if(entree[0]!='0'):
                        if(len(entree)>8):
                            updateType(i,'BIGINT',entree)
                            isInt=True
                        if(len(entree)<9):
                            updateType(i,'INT',entree)
                            isInt=True
                    if(entree[0]=='0'):
                        if(len(entree)>8):
                            updateType(i,'STRING',entree)
                        if(len(entree)<2):
                            updateType(i,'INT',entree)
                            isInt=True
                if isFloat(entree) and not(entree[0]=='0' and len(entree)>1 and entree[1]!=',') and not(isInt):
                    updateType(i,'FLOAT',entree)
                elif isDate(entree):
                    updateType(i,'DATE',entree)
                elif not(isInt):
                    #print(entree)
                    updateType(i,'STRING',entree)
                    #quit()
                #print(entree,tabType[i][0],tabType[i][1],tabType[i][2])
        entrees=f.readline()
                    
        for i in range(len(tabType)):
            if tabType[i][2]=='aucuneVAL':
                tabType[i][1]='STRING'
                tabType[i][2]='AUCUNE VALEUR TROUVEE DANS LE FICHIER'

    for col in tabType:
        print("nom col : "+col[0])
        print("type col : "+col[1]+" / val : "+col[2])
        print()

    #definition de fin des requêtes
    last="""
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '"""+separateurEchape+"""' COLLECTION ITEMS TERMINATED BY '\\002' MAP KEYS TERMINATED
BY '\\003'
LINES TERMINATED BY '\\n'
STORED AS TEXTFILE;"""
            
    req="CREATE TABLE "+filename[:-4]+" ("
    for col in tabType:
        req+=col[0]+" "+col[1]+","
    req=req[:-1]
    req+=")"+last
    print(req)
    reqTot.append(req)
print("\n********************************************************")
print("fin de traitement / recap")
print("********************************************************")
print("** debut req sql **")
print("*******************")

for req in reqTot:
    print(req)
print("*****************")
print("** fin req sql **")
print("*****************")
print("** separateur  **")
print("*****************")
print(sepFichier)
input()
