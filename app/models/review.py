from pydantic import BaseModel, Field
from typing import Annotated

class Review(BaseModel): 
    review: Annotated[int, Field(ge=1, le=5)] # review deve essere compreso tra 1 e 5
    # se arriva un numero minore di 1 o maggiore di 5
    # solleva un'eccezione, vogliamo personalizzare il messaggio
    # di errore
    # quindi modifichiamo da Field a con validator



