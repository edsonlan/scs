import pandas as pd 
import os
import sys
import colour


 
columns_to_keep = [
#Idenficicacao    
#'Código Horizonte',
#'Símbolo Horizonte',
#'Número PA'
#'Código PA',
 #Profundidade
#'Profundidade Superior',
#'Profundidade Inferior',
#Drenagem
'Classe de drenagem',
 #Fisico-Quimica                  
'Atividade da argila', #Categorico
'Saturação por bases ou por alumínio', #Categorico
'pH - H2O',
'Ataque sulfúrico - SiO2 / Al2O3 (Ki)',
'Carbono orgânico',
#Cor/Textura
'Classe de Textura', #Categorico
'Cor da Amostra Úmida - Matiz',
'Cor da Amostra Úmida - Valor',
'Cor da Amostra Úmida - Croma',
'Cor da Amostra Amassada - Matiz',
'Cor da Amostra Amassada - Valor',
'Cor da Amostra Amassada - Croma',
'Cor da Amostra Seca - Matiz',
'Cor da Amostra Seca - Valor',
'Cor da Amostra Seca - Croma',
'Cor da Amostra Seca Triturada - Matiz',
'Cor da Amostra Seca Triturada - Valor',
'Cor da Amostra Seca Triturada - Croma',
#Granulometria
'Frações da Amostra Total - Calhaus (g/Kg)',
'Frações da Amostra Total - Cascalho (g/Kg)',
'Frações da Amostra Total - Terra Fina (g/Kg)',
'Composição Granulométrica da terra fina - Areia Grossa (g/Kg)',
'Composição Granulométrica da terra fina - Areia Fina (g/Kg)',
'Composição Granulométrica da terra fina - Areia Total (g/Kg)',
'Composição Granulométrica da terra fina - Silte (g/Kg)',
'Composição Granulométrica da terra fina - Argila (g/Kg)',
'Composição Granulométrica da terra fina - Relação Silte Argila (g/Kg)',
'Composição Granulométrica da terra fina - Argila Dispersa em Água (g/Kg)',
#Classificacao Nivel 1 
'Classe de Solos Nível 1'

]

drenagem_class = {"Classe de drenagem": {"Excessivamente drenado":14, 
                                         "Fortemente a excessivamente drenado":13,
                                         "Fortemente drenado":12,
                                         "Acentuadamente a fortemente drenado":11,  
                                         "Acentuadamente drenado":10,
                                         "Bem a acentuadamente drenado":9,
                                         "Bem drenado":8, 
                                         "Moderadamente a bem drenado":7,
                                         "Moderadamente drenado":6,
                                         "Imperfeitamente a moderadamente drenado":5,
                                         "Imperfeitamente drenado":4,
                                         "Imperfeitamente a mal drenado":3,
                                         "Mal drenado":2, 
                                         "Mal drenado a muito mal drenado":1,
                                         "Muito mal drenado":0}
}

atividade_argila_class = {'Atividade da argila':{'Ta':1,'Tb':0}
                          }


saturacao_bases_class= {'Saturação por bases ou por alumínio':{'hipereutrófico':8,
                                                              'Eutrófico':7,
                                                              'mesoeutrófico':5,
                                                              'epieutrófico':6,
                                                              'hiperdistrófico':5,
                                                              'Distrófico':4,
                                                              'mesodistrófico':3,
                                                              'epidistrófico':2,
                                                              'Álico':1,
                                                              'epiálico':0}
                     }


texture_class = {'Classe de Textura':{
    
'Areia':17
,'Areia-franca com cascalho':16
,'Areia-franca':15
,'Franco-arenosa com cascalho': 14
,'Franco-arenosa':13
,'Franca muito cascalhenta':12
,'Franca com cascalho':12
,'Franco-argilo-arenoso m. cascalhenta':11
,'Franco-argilo-arenosa com cascalho':10
,'Franco-argilo-arenosa':9
,'Franco-argilosa com cascalho':8
,'Franco-argilosa':7
,'Franco-arenosa cascalhenta' :6
,'Argilo-arenosa cascalhenta':5
,'Argilo-arenosa':4
,'Argilo-siltosa':3
,'Argila com cascalho':2
,'Argila':1
,'Muito argilosa (argila pesada)':0
}
    
}


def clean_data (dataframe,columns_to_keep):
    
    return dataframe[columns_to_keep]

def map_categorical (dataframe,class_map):
    
    return dataframe.replace(class_map)

def convert_munsell_color (matiz_column,value_column,chroma_column):
    matiz = matiz_column.replace(',','.')
    value = value_column
    chroma = chroma_column
    munsell_color = matiz + " " +str(value)+"/" + str(chroma)
    color = colour.xyY_to_XYZ(colour.munsell_colour_to_xyY(munsell_color))
    return color

def map_colors(dataframe):
 for index in dataframe.index:
     try:
      XYZ_color_amostra_seca = convert_munsell_color(dataframe.loc[index]['cor_amostra_seca_matiz'],dataframe.loc[index]['cor_amostra_seca_valor'],dataframe.loc[index]['cor_amostra_seca_croma'])
      dataframe['cor_amostra_seca_X']=XYZ_color_amostra_seca[0]
      dataframe['cor_amostra_seca_Y']=XYZ_color_amostra_seca[1]
      dataframe['cor_amostra_seca_Z']=XYZ_color_amostra_seca[2]
      
      XYZ_color_amostra_umida = convert_munsell_color(dataframe.loc[index]['cor_amostra_umida_matiz'],dataframe.loc[index]['cor_amostra_umida_valor'],dataframe.loc[index]['cor_amostra_umida_croma'])
      dataframe['cor_amostra_umida_X']=XYZ_color_amostra_umida[0]
      dataframe['cor_amostra_umida_Y']=XYZ_color_amostra_umida[1]
      dataframe['cor_amostra_umida_Z']=XYZ_color_amostra_umida[2]
      
      XYZ_color_amostra_amassada = convert_munsell_color(dataframe.loc[index]['cor_amostra_amassada_matiz'],dataframe.loc[index]['cor_amostra_amassada_valor'],dataframe.loc[index]['cor_amostra_amassada_croma'])
      dataframe['cor_amostra_amassada_X']=XYZ_color_amostra_amassada[0]
      dataframe['cor_amostra_amassada_Y']=XYZ_color_amostra_amassada[1]
      dataframe['cor_amostra_amassada_Z']=XYZ_color_amostra_amassada[2]
           
      XYZ_color_amostra_seca_triturada = convert_munsell_color(dataframe.loc[index]['cor_amostra_seca_triturada_matiz'],dataframe.loc[index]['cor_amostra_seca_triturada_valor'],dataframe.loc[index]['cor_amostra_seca_triturada_croma'])
      dataframe['cor_amostra_seca_triturada_X']=XYZ_color_amostra_seca_triturada[0]
      dataframe['cor_amostra_seca_triturada_Y']=XYZ_color_amostra_seca_triturada[1]
      dataframe['cor_amostra_seca_triturada_Z']=XYZ_color_amostra_seca_triturada[2]
         
     except:
      #It an error occurs then remove the register 
      dataframe.drop(index=index,inplace=True)
      
 dataframe.drop(['cor_amostra_seca_matiz','cor_amostra_seca_valor','cor_amostra_seca_croma'],axis=1,inplace=True)
 dataframe.drop(['cor_amostra_umida_matiz','cor_amostra_umida_valor','cor_amostra_umida_croma'],axis=1,inplace=True)
 dataframe.drop(['cor_amostra_amassada_matiz','cor_amostra_amassada_valor','cor_amostra_amassada_croma'],axis=1,inplace=True)
 dataframe.drop(['cor_amostra_seca_triturada_matiz','cor_amostra_seca_triturada_valor','cor_amostra_seca_triturada_croma'],axis=1,inplace=True)


def load_data(path):

 os.chdir(path) 
 dataframe= pd.DataFrame() 
 
 for file in os.listdir(): 
     
     if file.endswith(".csv"): 
         file_path = f"{path}{os.sep}{file}"
         temp_dataframe = pd.read_csv(file_path,sep=";",low_memory=False)
         dataframe= pd.concat([dataframe,temp_dataframe])
    
 return dataframe

def clean_column_names(dataframe):
    
 dataframe.columns= map(str.lower,dataframe.columns)
  
 dataframe.columns=dataframe.columns.str.replace(' da ','_')
 dataframe.columns=dataframe.columns.str.replace(' do ','_')
 dataframe.columns=dataframe.columns.str.replace(' de ','_')
 dataframe.columns=dataframe.columns.str.replace(' - ','_')
 dataframe.columns=dataframe.columns.str.replace(' ','_')
 
 dataframe.columns=dataframe.columns.str.replace('ú','u')
 dataframe.columns=dataframe.columns.str.replace('ç','c')
 dataframe.columns=dataframe.columns.str.replace('â','a')
 dataframe.columns=dataframe.columns.str.replace('í','i')
 dataframe.columns=dataframe.columns.str.replace('õ','o')
 dataframe.columns=dataframe.columns.str.replace('ã','a')
 dataframe.columns=dataframe.columns.str.replace('á','a')
 dataframe.columns=dataframe.columns.str.replace('é','e')
 dataframe.columns=dataframe.columns.str.replace('ó','o')
 
 return dataframe

def main():
    
    #Dir with csv files with data
    input_dir = sys.argv[1]
    
    #Output file with dataframe
    output_file = sys.argv[2]
    
    all_data= load_data(input_dir)
    all_data = map_categorical(all_data,texture_class)
    
    #Kepping only some columns
    dataframe = clean_data(all_data,columns_to_keep)
    
    #Mapping some categorical attributes to numerical 
    dataframe = map_categorical(dataframe,drenagem_class)
    dataframe = map_categorical(dataframe,atividade_argila_class)
    dataframe = map_categorical(dataframe,saturacao_bases_class)
    
    #Renaming column names
    dataframe = clean_column_names(dataframe)
    
    #Removing registers without classification . Mandatory ?
    
    dataframe = dataframe.dropna(subset='classe_solos_nivel_1')
    
    
    
    
    #Removing registers with Nan, for now 
    dataframe= dataframe.dropna()
    dataframe.reset_index(inplace=True)
    
    #Mapping sample colors from Munsell to XYZ
    map_colors(dataframe)
    
    #Dropping index column
    dataframe.drop(['index'],axis=1,inplace=True)
        
    dataframe.to_csv(output_file,sep=';',index=False)

if __name__ == "__main__":
    main()



