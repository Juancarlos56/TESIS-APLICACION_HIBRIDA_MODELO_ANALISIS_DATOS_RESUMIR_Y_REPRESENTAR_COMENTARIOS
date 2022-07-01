###Librerias de transformador
from transformers import (
    T5ForConditionalGeneration,
    T5TokenizerFast as T5Tokenizer,
)

import torch

class TextSummarizationPredict:
    """ Clase TextSummarizationPredict """
    
    def __init__(self) -> None:
        """ Inicia la clase TextSummarizationT5 """
        pass

    def load_model(
      self, model_type: str = "t5", model_dir: str = "outputs", use_gpu: bool = False
    ):
        """
          carga un punto de control para inferencia/predicción
          Args:
              model_type (str, optional): "t5".
              model_dir (str, optional): ruta al directorio del modelo. Default "outputs".
              use_gpu (bool, optional): if True, el modelo usa gpu para inferencia/predicción. 
                                        Default True.
        """
        if model_type == "t5":
            self.model = T5ForConditionalGeneration.from_pretrained(f"{model_dir}")
            self.tokenizer = T5Tokenizer.from_pretrained(f"{model_dir}")

        if use_gpu:
            if torch.cuda.is_available():
                self.device = torch.device("cuda")
            else:
                raise "exception ---> no gpu found. set use_gpu=False, to use CPU"
        else:
            self.device = torch.device("cpu")

        self.model = self.model.to(self.device)

    def predict(
            self,
            source_text: str,
            max_length: int = 32,
            num_return_sequences: int = 1,
            num_beams: int = 2,
            top_k: int = 50,
            top_p: float = 0.95,
            do_sample: bool = True,
            repetition_penalty: float = 2.5,
            length_penalty: float = 1.0,
            early_stopping: bool = True,
            skip_special_tokens: bool = True,
            clean_up_tokenization_spaces: bool = True,
        ):
        
        """
            Genera predicción para el modelo T5
            Args:
              source_text (str): texto para generar predicción
              max_length (int, optional): longitud máxima del token de predicción.
              num_return_sequences (int, optional): número de predicciones a devolver. 
                                                    Default 1.
              num_beams (int, optional): numero de beams. Default 2.
              top_k (int, optional): Default 50.
              top_p (float, optional): Default 0.95.
              do_sample (bool, optional): Default True.
              repetition_penalty (float, optional): Defaults 2.5.
              length_penalty (float, optional): Defaults 1.0.
              early_stopping (bool, optional): Defaults True.
              skip_special_tokens (bool, optional): Defaults True.
              clean_up_tokenization_spaces (bool, optional): Defaults True.
            Returns:
              list[str]: returns predicción
        """
        input_ids = self.tokenizer.encode(source_text, return_tensors="pt", add_special_tokens=True)
        input_ids = input_ids.to(self.device)
        generated_ids = self.model.generate(
          input_ids=input_ids,
          num_beams=num_beams,
          max_length=max_length,
          repetition_penalty=repetition_penalty,
          length_penalty=length_penalty,
          early_stopping=early_stopping,
          top_p=top_p,
          top_k=top_k,
          num_return_sequences=num_return_sequences,
        )
        preds = [
            self.tokenizer.decode(
              g,
              skip_special_tokens=skip_special_tokens,
              clean_up_tokenization_spaces=clean_up_tokenization_spaces,
            )
            for g in generated_ids
        ]
        return preds