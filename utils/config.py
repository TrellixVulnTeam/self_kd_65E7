import os
import yaml
import shutil
from utils.utils import Logger

class Config(object):
    """ default param setting
    """

    def __init__(self, args) -> None:

        # training setting
        self.args = args
        self.gpu: str = args.gpu
        self.exp_name: str = args.exp_name
        self.seed: int = args.seed
        self.num_workers: int = args.num_workers
        self.resume: str = args.resume

        self.dataset: str = args.dataset
        self.method: str = args.method
        self.backbone: str = args.backbone
        self.epochs: int = args.epochs
        self.optim: str = args.optim.lower()
        self.wd: float = args.wd
        self.batch_size: int = args.batch_size
        self.t: float = args.t
        self.p: float = args.p
        self.alpha: float = args.alpha
        self.beta: float = args.beta
        self.detach: bool = args.detach
        self.aug: bool = args.aug

        self.prefetch: int = 2

        # hyper-params
        self.hyper_param = {
            'method': '',
            'batch_size': 'B',
            'p': 'p',
            't': 't',
            'alpha': 'alpha',
            'beta': 'beta',
            'wd': 'wd',
            'optim': '',
            'detach': 'detach',
            'seed': 'seed',

            # 'lr': 'Lr',
            # 'lr_schedule': 'LR_Schedule_',
            # 'weight_decay': 'WD',
        }

        # if self.method == 'posenet':
        #     self.hyper_param.update(
        #         {
        #             'backbone': '',
        #             'model_type': '',
        #             'output_shape': 'Osize',
        #             'deconv_layer_num': 'DeconvN',
        #         }
        #     )
        # elif self.method == 'unipose':
        #     self.hyper_param.update(
        #         {
        #             'pretrained_name': '',
        #         }
        #     )

        ## type hint
        # self.logfile: str
        # self.save_folder: str
        # self.tb_folder: str
        self.logger: Logger

        self.build()

    def __str__(self) -> str:
        _str = "==== params setting ====\n"
        for k, v in self.__dict__.items():
            if k == 'args': continue
            _str += f"{k} : {v}\n"
        return _str

    def set_params(self, params: dict) -> None:
        for k, v in params.items():
            self.__setattr__(k, v)

    def build(self):
        """ 
        expname 재정의 
        log/tb dir 만들기
        """

        for k, v in self.hyper_param.items():
            self.exp_name += f"_{v}{self.__getattribute__(k)}"

        if self.exp_name[0] == '_': self.exp_name = self.exp_name[1:]

        self.save_folder = os.path.join('saved_models', self.exp_name)
        self.tb_folder = os.path.join('tb_results', self.exp_name)

        if os.path.exists(self.save_folder) or os.path.exists(self.tb_folder):
            print(f"Current Experiment is : {self.exp_name}")
            isdelete = input("delete exist exp dir (y/n): ")
            if isdelete == "y":
                if os.path.exists(self.save_folder): shutil.rmtree(self.save_folder) 
                if os.path.exists(self.tb_folder):   shutil.rmtree(self.tb_folder) 
            elif isdelete == "n":
                raise FileExistsError
            else:
                raise FileExistsError

        os.makedirs(self.save_folder, exist_ok=True)
        os.makedirs(self.tb_folder, exist_ok=True)
        ## logfile
        self.logfile = os.path.join(self.save_folder, 'log.txt')

        self.save()

    def save(self) -> None:
        """
        attribute들 
        실험 dir에 yaml 파일로 저장.
        """
        yaml_path = os.path.join(self.save_folder, "params.yaml")
        with open(yaml_path, 'w') as f:
            yaml.dump(self.__dict__, f)
