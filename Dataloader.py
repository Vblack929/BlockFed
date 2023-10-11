import torch
from torchvision import datasets, transforms

class DataLoader:
    def __init__(self, dataset_name="Mnist"):
        self.dataset_name = dataset_name
        self.root_dir = "./" + self.dataset_name + "_data"
        if self.dataset_name == "Mnist":
            self.transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])
        else:
            self.transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])
        
        
    def get_mnist_loaders(self, train_batch_size, test_batch_size):
        """download and load the mnist dataset and return the dataloaders

        Args:
            train_batch_size (int): batch size for training
            test_batch_size (int): batch size for testing
        
        Returns:
            train_loader (DataLoader): dataloader for training
            test_loader (DataLoader): dataloader for testing
        """
        
        train_set = datasets.MNIST('./Mnist_data', train=True, download=True, transform=self.transform)
        train_loader = torch.utils.data.DataLoader(train_set, batch_size=train_batch_size, shuffle=True)
        
        test_set = datasets.MNIST('./Mnist_data', train=False, download=True, transform=self.transform)
        test_loader = torch.utils.data.DataLoader(test_set, batch_size=test_batch_size, shuffle=True)
        
        return train_loader, test_loader


