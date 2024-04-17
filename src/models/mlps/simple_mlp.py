import torch.nn as nn
import torch
from models.activation_parsing import get_activation


class SimpleMlp(nn.Module):
    def __init__(self, 
                 input_dim: int,
                 hidden_layers_out_features: list,
                 use_batch_norm: bool,
                 hidden_activation_function_name: str,
                 output_activation_function_name: str,
                 out_dim: int):
        super().__init__()
        
        in_features = input_dim
        self.hidden_layers = nn.ModuleList()
        for hidden_layer_out_features in hidden_layers_out_features:
            layer = [nn.Linear(in_features=in_features, out_features=hidden_layer_out_features)]
            if use_batch_norm:
                layer.append(nn.BatchNorm1d(num_features=hidden_layer_out_features))
            self.hidden_layers.append(nn.Sequential(*layer))
            in_features = hidden_layer_out_features
        
        self.hidden_activation_function_name = hidden_activation_function_name
        self.output_activation_function_name = output_activation_function_name
        
        self.output_layer = nn.Linear(in_features=in_features, out_features=out_dim)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        for hidden_layer in self.hidden_layers:
            activation_function = get_activation(self.hidden_activation_function_name)
            x = activation_function(hidden_layer(x))
        
        activation_function = get_activation(self.output_activation_function_name)
        
        return activation_function(self.output_layer(x))