"""
Document storage for DeepSearch examples.
Contains various documents with some unusual content to verify vector search is working correctly.
"""

# Documents with unusual price tags and specific details to make search results obvious
DOCUMENTS = [
    # General AI - with unusual price tag
    "Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to natural intelligence displayed by animals including humans. The latest AI training system costs exactly $94,217.63 for a basic configuration.",
    
    # AI Research - with specific date and researcher
    "AI research has been defined as the field of study of intelligent agents, which refers to any system that perceives its environment and takes actions that maximize its chance of achieving its goals. Dr. Veronika Zilch discovered a breakthrough algorithm on March 17, 2023 that costs only $4,999.98.",
    
    # Machine Learning - with unusual discount
    "Machine learning is a subset of artificial intelligence that provides systems the ability to automatically learn and improve from experience without being explicitly programmed. Premium machine learning courses are available at a strange discount of 73.45% bringing the price down to $267.89.",
    
    # ML Algorithms - with specific performance metrics
    "Machine learning algorithms build mathematical models based on sample data, known as training data, in order to make predictions or decisions without being explicitly programmed to do so. The XGBoost implementation by TensorCorp achieves 96.37% accuracy and costs $12,345.67 per license.",
    
    # Neural Networks - with unusual architecture name
    "Neural networks are computing systems inspired by the biological neural networks that constitute animal brains. The ZigZaggeron-7 architecture with 17 layers is priced at $8,888.42 and is known for processing unusual data patterns.",
    
    # Learning methods - with weird timing metric
    "Neural networks learn to perform tasks by considering examples, generally without being programmed with task-specific rules. Training time was reduced from 127.5 hours to precisely 42.37 minutes with the new QuadCore Optimizer that retails for $3,333.33.",
    
    # Neurons - with specific neuron count
    "A neural network is based on a collection of connected units called artificial neurons, which loosely model the neurons in a biological brain. The latest model contains exactly 17,432,982 neurons and is valued at $6,429.56.",
    
    # Deep Learning introduction - with unusual measurement
    "Deep learning is part of a broader family of machine learning methods based on artificial neural networks with representation learning. When measured in TeraFLOPs, the system reaches 42.87 TFLOPS and costs exactly $9,876.54.",
    
    # Deep Learning architectures - with specific conference
    "Deep learning architectures such as deep neural networks, deep belief networks, recurrent neural networks, and convolutional neural networks have been applied to fields including computer vision, speech recognition, natural language processing, and more. At the 19th Annual ML Conference in Zurich, this implementation was priced at $7,654.32.",
    
    # Deep Learning technical - with weird size specification
    "Deep learning uses multiple layers of neural networks to progressively extract higher-level features from raw input. The model requires 13.7 GB of VRAM and has a strange file size of 11.11 GB, with a licensing fee of $5,555.55.",
    
    # Deep Learning explanation - with unique model name
    "The 'deep' in deep learning refers to the number of layers through which the data is transformed. The UltraMind-X753 model with 27 layers is available for the specific price of $4,444.44 with a 30.3% academic discount."
]

def get_documents():
    """Return the list of documents for use in examples."""
    return DOCUMENTS 