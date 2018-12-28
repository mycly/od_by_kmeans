import pandas as pd
from sklearn.cluster import KMeans
#df = pd.read_csv("/data/ChenLei/xian_didi/xian/gps_20161121",names=['driverid', 'orderid', 'timestamp', 'longitude', 'latitude'])
#df=df.groupby('orderid').apply(lambda row: row[(((row.timestamp==row.timestamp.max()) & ((row.timestamp!=row.timestamp.min())) )|((row.timestamp==row.timestamp.min()) & ((row.timestamp!=row.timestamp.max())) ))  ])
#df.to_csv('even_OD.csv')
df=pd.read_csv('even_OD.csv')
df=df[['longitude', 'latitude']]

for i in range(100,251,10):
    db=KMeans(n_clusters=i,n_jobs=-1).fit_predict(df)
    plt.figure(figsize=(100, 100),dpi=80)
    plt.scatter(df['longitude'],df['latitude'], c=y_pred, s=1, alpha=0.3)
    fig_str='eps:kmeans{i}m.png'.format(i=i)
    plt.savefig(fig_str)
    df1=pd.DataFrame(data=db)
    files_str='kmeans{i}m.csv'.format(i=i)
    df1.to_csv(files_str)

final_tables=pd.DataFrame(columns=['噪声点占OD点比例','自环边比例','自环区域比例','完全图边比例'])
for i in range(100,251,10):
    a=[]
    files_str='kmeans{i}m.csv'.format(i=i)
    df=pd.read_csv(files_str)
    a.append((len(df[df['0']==(-1)]))/len(df))
    df1=pd.read_csv('even_OD.csv')
    df['orderid']=df1['orderid']
    df=df[['0','orderid']]
    df_O=df.drop_duplicates(subset=['orderid'],keep='first')
    df_O.columns = ['O_labels','orderid']
    df_O = df_O.reset_index(drop=True)
    df_D=df.drop_duplicates(subset=['orderid'],keep='last')
    df_D.columns = ['D_labels','orderid']
    df_D = df_D.reset_index(drop=True)
    df_OD=df_O
    df_OD['D_labels']=df_D['D_labels']
    df_OD=df_OD[['orderid','O_labels','D_labels']]
    files_str='kmeans{i}m{j}_div.csv'.format(i=i,j=j)
    df.to_csv(files_str)

        #自环边比例，包含噪声点在内
    loop_edge=df_OD[df_OD['O_labels']==df_OD['D_labels']]
    a.append(len(loop_edge)/len(df_OD))
        #print('自环边比例：{ratio}'.format(ratio=len(loop_edge)/len(df_OD)))
        #自环区域比例，除噪声点外
    loop_dist=loop_edge.drop_duplicates(subset=['O_labels','D_labels'],keep='first')
    a.append(len(loop_dist)/((df_OD['O_labels'].max())+1 ))
        #print('自环区域比例：{ratio}'.format(ratio=len(loop_dist)/((df_OD['O_labels'].max())+1 )))
        #完全图边数量与边数量之比
    compl_gra=df_OD[df_OD['O_labels']!=df_OD['D_labels']]
    compl_gra=compl_gra[['O_labels','D_labels']]
    compl_gra=compl_gra.drop_duplicates(subset=['O_labels','D_labels'],keep='first')
    df_compl_gra=compl_gra[['D_labels','O_labels']]
    df_compl_gra.columns=['O_labels','D_labels']
    df_compl_final=pd.concat([df_compl_gra,compl_gra])
    df_compl_final=df_compl_final.drop_duplicates(subset=['O_labels','D_labels'],keep=False)
    a.append(len(df_compl_final/2)/len(df_OD))
    b = pd.DataFrame(a).T
    b.columns = final_tables.columns
    final_tables=final_tables.append(b)
        #print('完全图边比例：{ratio}'.format(ratio=len(df_compl_final/2)/len(df_OD)))
final_tables.to_csv('kmeans_final_tables.csv')