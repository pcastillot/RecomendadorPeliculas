import pandas
import dbManager
import pickle


queryPeliculas = dbManager.getPeliculas()
peliculas = []
for pelicula in queryPeliculas:
    peliculas.append(pelicula[1])

#print(peliculas)

queryUsuarios = dbManager.getUsuarios()
usuarios = []
for usuario in queryUsuarios:
    usuarios.append(int(usuario[0]))

#print(usuarios)

df = pandas.DataFrame(columns=peliculas)

for usuario in usuarios:
    ratingsUsuario = dbManager.getRatingsUsuario(usuario)
    media = 0.0
    #print(ratingsUsuario)
    for rating in ratingsUsuario:
        media += float(rating[2])

    media = media/len(ratingsUsuario)
    mediaString = str(format(media, ".3f"))

    ratingsFinal = {}

    for rating in ratingsUsuario:
        ratingNuevo = float(rating[2]) - media
        update = {str(rating[1]): ratingNuevo}
        ratingsFinal.update(update)

    df = df.append(ratingsFinal, ignore_index=True)

    print(df)

    print("\nusuario: " + str(usuario) + "/" + str(len(usuarios)) + " ---- " + str(
        format((usuario * 100) / len(usuarios), ".2f")) + "%\n")

print(df)

pickle.dump(df, open("dataframe.p", "wb"))




