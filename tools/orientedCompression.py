import torch
import torch.nn as nn
import torch.optim as optim

class OrientedCompression():
    def __init__(self, model:nn.Module, *filter):
        self.model = model
        self.dic = self.getParamMap(model, *filter)

    @staticmethod
    def getParamMap(model:nn.Module, *filters):
        freeze_weights = []
        
        for name, module in model.named_modules():
            if (not isinstance(module, nn.Conv2d)): continue
            
            cnt = 0
            weight = module.weight 
            for out_ch in range(weight.shape[0]):
                for in_ch in range(weight.shape[1]):
                    for i in range(weight.shape[2]):
                        for j in range(weight.shape[3]):
                            key = [out_ch, in_ch, i, j]
                            val = weight[*key].item()
                            
                            for func in filters:
                                if (not func(val)): break
                            else:
                                freeze_weights.append((key, val))
                                cnt += 1
            
            print(f"Conv Layer: {name}, Weight shape: {weight.shape} / selected params: {cnt}")
        
        return freeze_weights
    
    def backward(self, fixed_value=None):
      with torch.no_grad():
          for (out_ch, in_ch, i, j), val in self.dic:
              val = fixed_value if (fixed_value is not None) else val
              self.model.conv.weight[out_ch, in_ch, i, j] = val
