#import functools         PARA CREAR WRAPPERS (@wrap.customname(wrapped_func.params))
from json import dumps
from colorama import Fore, Back, Style #, init
from random import randint, choice



def cFormatter(
    string: str, 
    color: Fore, 
    style: Style = None, 
    background: Back = None, 
    random: bool = False, 
    iter_colors: list[Fore] = []
) -> str:
    """
    Formateador de texto en terminal.
    Valido con cadenas de texto, listas de texto y docstrings.
    """
    
    #init(autoreset= autoreset)

    c = [Fore.BLACK, Fore.RED, Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.MAGENTA, Fore.YELLOW, Fore.WHITE]
    s = [Style.DIM, Style.NORMAL, Style.BRIGHT]
    b = [Back.BLACK, Back.RED, Back.BLUE, Back.CYAN, Back.GREEN, Back.MAGENTA, Back.YELLOW, Back.WHITE]

    if (color is not None and not color in c) or (style is not None and not style in s) or (background is not None and not background in b):
        return ValueError(cFormatter(f"Color o estilo o fondo no valido", color= Fore.RED))

    else:

        if iter_colors:
            if len(iter_colors) == 0 or [x for x in iter_colors if x not in c]:
                return TypeError(cFormatter("No se ha definido una lista de colores con los que iterar o algun color no es valido", color= Fore.RED))
            else: 
                letters = []
                for chars in string:
                    letters.append(f"{choice(iter_colors)}{chars}{Fore.RESET}")
                return "".join(letters)

        elif random:
            rcolor = choice(c)
            rstyle = choice(s)
            rback = choice(b)
            return f"{rcolor}{rstyle}{rback}{string}{Style.RESET_ALL}{Fore.RESET}{Back.RESET}"

        elif color:
            if background:
                return f"{color}{background}{string}{Fore.RESET}{Back.RESET}"
            elif style:
                return f"{color}{style}{string}{Fore.RESET}{Style.RESET_ALL}"
            else:
                return f"{color}{string}{Fore.RESET}"





class Furniture:

    materials: list[str] = ["Wood", "Metal", "Oak", "Sequoia"]

    def __init__(
        self,
        paws: int,
        screws: int,
        pieces: int,
        material: str | list[str] = ["Wood", "Metal", "Oak", "Sequoia"]
    ):
        self.paws = paws
        self.screws = screws
        self.pieces = pieces
        self.material = [material.capitalize()] if not isinstance(material, list) else [m.capitalize() for m in material]
    
    #* Este metodo privado solo puede retornar un str, cuando printeas una instancia de clase (no la clase print(Furniture)) __str__ sera llamado
    def __str__(self):
        for m in self.materials:
            return m

    #* Metodo para comprobar si un objeto es una subclase de Furnitures
    @classmethod
    def is_subclass(cls, obj) -> bool:
        return isinstance(obj, cls)

    #* Metodo para añadir un material a la clase Furnitures sin necesidad de instanciar un objeto de clase
    @classmethod
    def add_material(cls, material: str | list[str]):
        cls.materials.append([m.capitalize() for m in material] if isinstance(material, list) else material)
        return f"Añadido correctamente el material {material}"


#* Creamos, a partir de la clase padre mueble, subclases de mueble que son diferentes tipos de muebles (Herencia)
#* Pasamos los argumentos de forma rapida pero indicando que se deben pasar todos los parametros de la clase Furniture (Padre)

class Tables(Furniture):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
class Wardrobes(Furniture):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
class Chairs(Furniture):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class Shop:
    furnitures = {"Furnitures": {"Tables": {}, "Wardrobes": {}, "Chairs": {}}, "External": []}
    fmodels: list[type] = [Tables, Wardrobes, Chairs]

    def _range_fvalues(self, value: int | str, dict: dict) -> str | int:
        return [dict.keys()][list(dict.values()).index(value)]


    def add_furniture(self, f: type):

        clsname: str = f.__class__.__name__
        for fm in self.fmodels:
            if isinstance(f, Furniture) and not f.__class__ in self.fmodels:
                self.fmodels.append(f.__class__)
                self.furnitures["Furnitures"][clsname] = {}
                pass

            if isinstance(f.__class__, fm.__class__):
                #TODO: El indice -1 de una lista indica el ultimo elemento del mismo (Asi con -2,-3 etc...). Dato interesante
                self.furnitures["Furnitures"][clsname][1 if len(self.furnitures["Furnitures"][clsname].keys()) <= 0 else (list(self.furnitures["Furnitures"][clsname])[-1])+1] = {
                    "Paws": f.paws, 
                    "Screws": f.screws, 
                    "Pieces": f.pieces, 
                    "Materials": f.material
                }
                return f"Objecto | {clsname} | guardado correctamente"
            else:
                raise Exception(f"----  La clase {clsname} no es una subclase de Furniture. ----")


    def del_forniture(self, key: int, value: str = None):
        if value:
            del self.furnitures[self._range_fvalues(value)]
            return f"Se ha eliminado correctamente {self.furnitures[self._range_fvalues(value)]}"
        else:
            try:
                del self.furnitures["Furnitures"][key]
            except KeyError:
                raise KeyError(f"----   La llave {key} no existe en el diccionario    ----")
            finally:
                return f"Se ha eliminado correctamente {self.furnitures['Furnitures'][key]}"
    

    def SearchFor(self, material: str | list[str] = None, paws: bool = None, screws: bool = None, pieces: bool = None):

        #* Este metodo es muy modificable, y no se si es exactasmente lo que quieres que haga
        #* Si lo que quieres es que tambien se permita la busqueda de dos parametros se puede hacer.

        coll_results = {"Tables": [], "Wardrobes": [], "Chairs": [], "Total Results": []}

        if material and paws or screws or pieces is not None:
            raise ValueError("----  Solo se puede buscar a traves de un solo parametro definido o no se ha definido ningun parametro.\nSi se pasan dos parametros a evaluar la funcion no funcionara o dará error.    ----") 

        elif isinstance(material, list):
            for m in material:
                if not m in Furniture.materials:
                    raise TypeError(f"----   Los materiales proporcionados no son válidos.\nMateriales válidos -> {[m for m in Furniture.materials]}    ----") 
        elif material is not None and not material in Furniture.materials:
            raise TypeError(f"----  | {material} | no es un material válido.\nMateriales válidos -> {[m for m in Furniture.materials]}    ----") 
        else:

            for fk in self.furnitures["Furnitures"]:
                for fv in self.furnitures["Furnitures"][fk].values():
                    if paws:
                        coll_results[fk].append(fv["Paws"])
                    elif screws:
                        coll_results[fk].append(fv["Screws"])

                    elif pieces:
                        coll_results[fk].append(fv["Pieces"])
                    else: 
                        if isinstance(material, list):
                            for m in material:
                                if m in fv["Materials"]:
                                    coll_results[fk].append(m)
                                pass
                        elif material in fv["Materials"]:
                            coll_results[fk].append(len([material]))
        coll_results["Total Results"].append(f"{sum([sum(coll_results[m]) for m in coll_results])} elementos ({[sum(coll_results[m]) for m in coll_results]})") 
        coll_results["Total Results"].append(f"Filtering for: {'Material' if material else 'Paws' if paws else 'Pieces' if pieces else 'Screws'}")
        return coll_results


    @property
    def show_data(self) -> dict:
        return dumps(
            self.furnitures,
            indent= 4
        )

#* //////// Instanciamos los objectos

# TODO: hago esto asi solo por una cuestion de limpieza, pero no esta exactamente bien hecho, but np.
f = {

    "t": Tables(paws= 6, screws= 40, pieces= 25, material= ["Wood", "Metal", "Sequoia"]),
    "t2": Tables(paws= 4, screws= 35, pieces= 20, material= ["Metal", "Oak"]),
    "t3": Tables(paws= 8, screws= 90, pieces= 10, material= ["Wood", "Metal", "Oak", "Metal"]),
    "t4": Tables(paws= 8, screws= 35, pieces= 20, material= ["Metal", "Oak"]),

    "w": Wardrobes(paws= 8, screws= 65, pieces= 40, material= ["Sequoia", "Metal", "Oak"]),
    "w2": Wardrobes(paws= 12, screws= 100, pieces= 50, material= ["Sequoia", "Metal"]),
    "w3": Wardrobes(paws= 10, screws= 65, pieces= 40, material= ["Sequoia"]),
    "w4": Wardrobes(paws= 20, screws= 145, pieces= 90, material= ["Sequoia", "Metal", "Metal", "Oak", "Maderica"]),

    "ch": Chairs(paws= 4, screws= 20, pieces= 10, material= "Oak"),
    "ch2": Chairs(paws= 3, screws= 10, pieces= 5, material= "Oak"),
    "ch3": Chairs(paws= 6, screws= 50, pieces= 20, material= ["Oak", "Maderica"]),
    "ch4": Chairs(paws= 2, screws= 9, pieces= 10, material= "Sequoia"),
}

c = Shop()
for f in f.values():
    print(c.add_furniture(f))

print(c.show_data)
print(c.SearchFor(paws=True))
print(Furniture.add_material('Maderica'))
print(Furniture.materials)





        
