'''
    The dimension of the feature is reduced.
'''
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import umap
from sklearn.preprocessing import StandardScaler

def getReDimFeature(Data, Label=None, **kwargs):
    '''
        Use different dimensionality reduction methods to obtain the reduced dimensional features.

        args:
            Data:Data requiring dimensionality reduction
            Label:The label corresponding to the data
            kwargs:
                ReDimFeature_kwargs:
                    Method:The dimensionality reduction method used
    '''
    ## 对数据进行标准化处理
    model=StandardScaler()
    Data_stand = model.fit_transform(Data)
    ReDimFeature_kwargs = kwargs["ReDimFeature_kwargs"]
    Method = ReDimFeature_kwargs["Method"]
    ## 降维
    if Method == "PCA":
        PCA_kwargs = ReDimFeature_kwargs["PCA_kwargs"]
        pca=PCA(n_components= PCA_kwargs["n_components"])#主成分数量为2，方便可视化
        features = pca.fit_transform(Data_stand)
    elif Method == "UMAP":
        UMAP_kwargs = ReDimFeature_kwargs["UMAP_kwargs"]
        if not Label.any():
            raise KeyError("Label value is not None")
        features = umap.UMAP(n_components= UMAP_kwargs["n_components"],
                             n_neighbors= UMAP_kwargs["n_neighbors"],
                             min_dist= UMAP_kwargs["min_dist"],
                             metric= UMAP_kwargs["metric"],
                             random_state= UMAP_kwargs["random_state"]
                            ).fit_transform(Data,Label)
    elif Method == "TSNE":
        TSNE_kwargs = ReDimFeature_kwargs["TSNE_kwargs"]
        features = TSNE(n_components= TSNE_kwargs["n_components"],
                        init= TSNE_kwargs["init"],
                        random_state= TSNE_kwargs["random_state"],
                        ).fit_transform(Data,Label)
    else:
        pass

    return features