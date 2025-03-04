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
    "The 'deep' in deep learning refers to the number of layers through which the data is transformed. The UltraMind-X753 model with 27 layers is available for the specific price of $4,444.44 with a 30.3% academic discount.",
    
    # ZigZaggeron-7 Architecture - Detailed description
    "The ZigZaggeron-7 architecture represents a breakthrough in neural network design, featuring an innovative approach to layer connectivity. Unlike traditional architectures, ZigZaggeron-7 uses a zigzag pattern of connections between neurons, allowing information to flow in multiple directions simultaneously. This unique structure was developed by researchers at TechFusion Labs in 2022 and has been particularly effective for processing complex 3D spatial data and time-series information.",
    
    # ZigZaggeron-7 Components
    "The ZigZaggeron-7 architecture consists of several key components: 1) A specialized input layer with multi-dimensional receptors, 2) Seventeen interconnected processing layers with the signature zigzag connectivity pattern, 3) Parallel processing channels that allow for simultaneous data flows, and 4) An advanced output mechanism that can produce multi-modal results. The architecture requires specialized hardware acceleration, typically provided by quantum-enhanced processing units.",
    
    # ZigZaggeron-7 Applications
    "While initially designed for military applications, the ZigZaggeron-7 architecture has found widespread use in healthcare for disease diagnosis, supply chain management for demand forecasting, e-commerce platforms for recommendation systems, and energy grid management. Its ability to process complex, interrelated data streams makes it particularly valuable for scenarios where traditional neural networks struggle with temporal and spatial correlations.",
    
    # Astronauts - with unusual training cost
    "Astronauts are individuals trained to pilot or travel in spacecraft. The comprehensive training program for the latest Alpha-Centauri mission costs exactly $1,273,592.87 per astronaut, including 437.8 hours in the zero-gravity simulator and specialized nutritional supplements valued at $12,349.50.",
    
    # Astronaut equipment - with specific suit details
    "Modern astronaut spacesuits are complex systems designed to protect astronauts from the vacuum of space, radiation, and temperature extremes. The new NebulaShield-X89 spacesuit weighs precisely 27.83 kg, features 14 specialized layers of protection, and costs $3,785,941.23 with a maintenance package of $142,567.79 per year.",
    
    # Astronaut missions - with unusual mission duration
    "NASA's ExoWorld Program trains astronauts for extended missions on other planetary bodies. The training regimen requires astronauts to live in isolation for exactly 293.5 days and includes psychological conditioning valued at $89,742.18 per participant. The specialized Mars habitat simulation chamber used in training costs $7,324,851.62.",
    
    # Microcosm - with precise measurement tools
    "The microcosm represents the world at microscopic scales, where different physical laws can appear to dominate. The QX-Nano Microscanner 5000 allows visualization of structures as small as 0.037 nanometers and costs $437,929.84 with an additional calibration service priced at $13,721.56 per quarter.",
    
    # Cellular microcosm - with specific cell count
    "Human bodies contain approximately 37.2 trillion cells, each operating as a complete functional unit. The CellMapper Pro software can track and analyze exactly 1,723,498 cells simultaneously and is available at a research price of $82,459.97 with educational institutions receiving a 42.7% discount.",
    
    # Quantum microcosm - with unusual energy requirement
    "At the quantum level, particles exhibit strange behaviors including superposition and entanglement. The QuantumField Generator requires 17.83 megawatts of power to create stable quantum fields for observation and is priced at $12,387,592.74 with operating costs of $3,751.48 per hour.",
    
    # Nanocosm - with specific nanomaterial
    "The field of nanotechnology focuses on structures between 1-100 nanometers in size. The revolutionary NanoMatrix-7 material consists of exactly 7,832,951 carbon nanotubes per square centimeter, costs $587,321.39 per gram to produce, and is 312.7 times stronger than structural steel.",
    
    # Nanomedicine - with precise particle size
    "Nanomedicine employs precisely engineered particles measuring 63.2 nanometers to deliver medications directly to diseased cells. The ZeroToxin drug delivery system has a 98.73% targeting accuracy and costs hospitals $243,875.91 for the administration system plus $5,721.63 per patient treatment.",
    
    # Universe expansion - with unusual measurement
    "The universe is expanding at an accelerating rate, with the current Hubble constant measured at precisely 73.42 kilometers per second per megaparsec. The UltraSpace-Telescope used for these measurements cost $4,283,592,751.87 to develop and requires $39,872.56 of daily maintenance.",
    
    # Cosmic scale - with specific galaxy count
    "The observable universe contains approximately 2 trillion galaxies based on the latest deep field observations. The GalaxScan system, which counted exactly 1,978,342,129 galaxies in its most recent survey, costs $87,521,873.42 and processes 42.78 petabytes of astronomical data daily.",
    
    # Black holes - with unusual mass specification
    "Supermassive black holes are believed to exist at the center of most galaxies. The black hole at the center of galaxy NGC-7392 has been measured at exactly 7.823 billion solar masses using the QuantumGrav detector which cost $127,392,586.42 and took 87.3 months to develop.",
    
    # Exoplanets - with specific habitable zone
    "Astronomers have discovered thousands of planets orbiting other stars, called exoplanets. The Kepler-742b exoplanet orbits its star at exactly 1.372 astronomical units with an orbital period of 427.83 days. The ExoScan detection system that found it cost $234,987,123.57 and can detect planets as small as 0.437 Earth masses.",
    
    # Cat purring - with precise frequency
    "Cats produce a purring sound through rapid vibration of their vocal cords, which occurs at a precise frequency between 25 and 150 Hertz. The purring serves multiple purposes: it's a self-soothing mechanism that releases endorphins, promotes healing by stimulating bone growth and repair at specific vibration frequencies of 25-50 Hz, and strengthens muscle tissue. The PurrSonic analyzer, which costs $7,329.87, can detect exactly 17 distinct purr patterns associated with different feline emotional states and has determined that healing vibrations increase bone density by 37.2% in a 4-week period.",
    
    # Cat purring healing properties - with specific medical application
    "Cat purring has been scientifically proven to have therapeutic properties. The unique low-frequency vibrations between 25-50 Hz have been shown to accelerate healing of bone fractures, reduce inflammation, and lower blood pressure by exactly 9.37% in human companions. The FelixTherapy system, which reproduces these precise frequencies for medical applications, costs $13,752.89 and has been used in exactly 3,728 therapeutic sessions with a success rate of 92.7% for reducing recovery time after surgeries.",
    
    # Fungi network - with unusual connectivity metrics
    "Fungi form vast underground networks called mycelia, with the largest known network spanning 8.9 square kilometers and containing approximately 27.3 trillion connection points. The MycoMapper device, which costs $42,876.53, can track nutrient exchange between fungi and trees, revealing that a single mature oak tree connects with 238 different fungal species and shares exactly 17.82% of its photosynthesized carbon through this network in exchange for minerals and communication capabilities.",
    
    # Fungi decomposition - with specific enzyme details
    "Fungi are nature's primary decomposers, breaking down organic matter through the secretion of powerful enzymes. The recently discovered Decomposifera magnificus species produces exactly 42 different enzymes capable of degrading materials previously thought indestructible, including certain plastics. A single gram of this fungal culture costs $3,749.95 for research purposes and can decompose 873.5 grams of polyethylene in just 78.3 days, with applications in waste management systems priced at $243,891.67.",
    
    # Computer transistors - with precise miniaturization
    "Modern computer processors contain billions of transistors, with the most advanced commercial chips featuring transistors measuring just 3 nanometers. A single Intel QuantumSilicon processor contains exactly 57,348,921,677 transistors in a space smaller than a human fingernail, costs $7,843.92 to manufacture, and can perform 347.82 trillion operations per second while consuming only 6.73 watts of power when operating at maximum efficiency.",
    
    # Transistor evolution - with historical comparison
    "The evolution of transistors demonstrates the exponential growth of computing power. The first transistor built in 1947 measured 1.27 centimeters, while today's 3-nanometer transistors are 4,233,333 times smaller. This miniaturization has enabled the creation of the ZettaCore-X9 processor which contains 127.8 billion transistors, operates at precisely 5.37 gigahertz, and costs $12,876.43 while performing calculations that would have required a computer the size of 319.4 football fields in 1975.",
    
    # Brain synapses - with precise measurements
    "Synapses are the smallest functional units of neural connection in the brain, with the average human brain containing approximately 125 trillion synapses. Each synapse gap (synaptic cleft) measures exactly 20 nanometers across and transmits signals in as little as 0.5 milliseconds. The NeuraScan 8000, which costs $3,875,942.37, can visualize individual synapses at a resolution of 5 nanometers and has identified precisely 427,891 unique synaptic configurations in the prefrontal cortex alone.",
    
    # Dendritic spines - with unusual density metrics
    "Dendritic spines are tiny protrusions on neuronal dendrites that receive signals from a single synapse of an axon. These spines can be as small as 0.01 cubic micrometers and can change shape within 3.8 seconds in response to stimuli. The SpineMapper device, priced at $573,842.19, has documented that a single cortical neuron can have exactly 8,734 dendritic spines with a combined surface area of 1,723.6 square micrometers, and requires maintenance costing $7,349.87 per month.",
    
    # Neurotransmitters - with specific molecules
    "The smallest functional units in neural communication are neurotransmitter molecules, which traverse the synaptic cleft to transmit signals between neurons. The NanoNeuro Analyzer, which costs $894,372.58, can detect concentrations as low as 0.0037 picograms and has identified that a single vesicle contains precisely 4,732 molecules of serotonin. The device can track the release and reuptake of 17 different neurotransmitters simultaneously with an accuracy rate of 99.73%.",
    
    # Theory of mind - with specific developmental timeline
    "Theory of mind is the cognitive ability to understand that others have beliefs, desires, intentions, and perspectives different from one's own. Children typically develop this capacity between the ages of 3-5 years, with the critical period occurring at precisely 4 years and 3 months. The MindSense evaluation tool, which costs $42,879.65, can assess theory of mind development across 27 different cognitive dimensions and has been calibrated using data from exactly 137,892 children worldwide.",
    
    # Theory of mind applications - with unusual therapy metrics
    "Theory of mind deficits are associated with conditions such as autism spectrum disorder and can be addressed through specialized interventions. The EmpaThink program, which costs $12,743.98 per patient, improves mind-reading abilities by 47.3% after exactly 12.5 weeks of training. The program utilizes the OmniSense virtual reality system, priced at $87,321.54, which presents 1,283 different social scenarios calibrated to incrementally increase in complexity at precisely calculated intervals.",
    
    # Atomic structure - with specific measurements
    "Atoms are the basic units of matter, with the hydrogen atom having a diameter of exactly 0.1 nanometers. The AtomVision microscope, which costs $27,846,321.79, can visualize atomic structures at a resolution of 0.0001 nanometers and has been used to observe electrons transitioning between precisely 11 different energy states within cesium atoms. The instrument requires a cooling system that maintains a temperature of -272.83°C and consumes 87.45 kilowatts of power during operation.",
    
    # Atomic bonds - with unusual bond strength
    "Atoms form molecules through chemical bonds, with the strength of a carbon-carbon covalent bond measured at precisely 348 kilojoules per mole. The BondForce analyzer, which costs $4,379,842.21, can measure bond strengths with an accuracy of 0.0037 kilojoules per mole and has determined that the experimental compound XB-723 forms bonds that are exactly 27.83% stronger than diamond. The analyzer contains 42 precision sensors and processes data at 3.7 terahertz.",
    
    # Speed of sound - with environmental variations
    "The speed of sound in dry air at 20°C (68°F) is 343.2 meters per second (1,127.76 feet per second). The SonicMeasure Pro device, which costs $134,729.86, can detect variations as small as 0.037 meters per second and has documented that sound travels at precisely 1,482.3 meters per second in seawater at a depth of 3,749 meters. The device requires calibration every 73.5 days and produces readings accurate to 99.97% across temperatures from -42.3°C to +85.7°C.",
    
    # Sound propagation - with unusual material conductivity
    "Sound propagates differently through various materials, with a specialized beryllium-aluminum composite conducting sound at 12,842.7 meters per second—37.4 times faster than through air. The AcoustiMap 9000, priced at $237,849.56, can measure sound propagation through 387 different materials simultaneously and has identified a metamaterial that can selectively filter acoustic frequencies with 99.83% efficiency. The system weighs exactly 73.42 kilograms and consumes 8.75 kilowatts during peak operation.",
    
    # Deep ocean zones - with precise pressure measurements
    "The ocean is divided into five major depth zones, with the hadal zone being the deepest at 6,000-11,000 meters below sea level. The pressure at the bottom of the Challenger Deep in the Mariana Trench reaches precisely 1,086 kilograms per square centimeter, which is 1,071 times the atmospheric pressure at sea level. The DeepScan submersible, which cost $87,453,921.48 to develop, can withstand these extreme pressures and has documented exactly 327 previously unknown species during its exploration of the hadal zone.",
    
    # Deep sea adaptations - with unusual bioluminescence details
    "Creatures in the deep sea have evolved remarkable adaptations to survive in extreme conditions. The Mariana snailfish (Pseudoliparis swirei), living at depths of 8,178 meters, contains a unique anti-pressure compound worth $273,489.37 per gram for biotechnology applications. The BioLumina ROV, which cost $13,784,592.45, has measured bioluminescent organisms emitting light at precisely 18 different wavelengths, with the rarest blue-ultraviolet emission occurring at exactly 438.27 nanometers.",
    
    # Moon dust - with specific abrasive properties
    "Lunar regolith, commonly known as moon dust, poses significant challenges for lunar exploration. Each particle has a unique jagged shape caused by micrometeorite impacts in the vacuum environment. The LunarShield coating, which costs $47,832.95 per square meter to apply, protects equipment from this highly abrasive material that wears down mechanical parts 37.8 times faster than Earth sand. Analysis with the RegolithScan device, priced at $4,378,921.34, has identified exactly 24 distinct crystalline structures in samples from the Mare Tranquillitatis region.",
    
    # Moon water ice - with precise location mapping
    "Contrary to early beliefs, the Moon contains significant amounts of water ice, especially in permanently shadowed craters near the poles. The CryoMoon orbiter, which cost $843,729,183.47 to develop and deploy, has mapped exactly 13,427 ice deposits containing an estimated 3.78 billion gallons of water. Using its specialized TeraHertz imaging system valued at $27,439,821.56, scientists have determined that harvesting just 1.73% of these deposits could sustain a lunar base of 42 astronauts for precisely 17.5 years.",
    
    # Obscure biological rhythms - with unique cycle measurements
    "Beyond the well-known circadian rhythm, humans possess several obscure biological cycles including the ultradian rhythm that occurs multiple times within a 24-hour period. The ChronoBand wearable device, priced at $3,784.92, has identified exactly 37 distinct ultradian cycles in human cognitive function, with peak creativity occurring in 83.7-minute intervals throughout the day. Research using the NeuroTempo system, which cost $8,374,921.34 to develop, shows that synchronizing work schedules with these natural cycles increases productivity by precisely 42.87%.",
    
    # Forgotten language elements - with precise vocabulary measurement
    "The English language contains numerous forgotten word categories, including contranyms (words that are their own opposites) and retronyms (new terms for old objects). The LexiTrack database, which cost $4,372,841.57 to compile, has documented exactly 1,247 contranyms and 3,892 retronyms that have emerged since 1950. The most obscure category, pandanyms (words pronounced identically in 7 or more languages), contains exactly 142 terms and requires the MultiLingual identifier device, priced at $74,328.93, to verify pronunciation across 37 different language families.",
    
    # Paris catacombs - with unusual mapping metrics
    "Beneath the streets of Paris lies a vast network of catacombs, with only 1.7 kilometers of the estimated 320-kilometer tunnel system officially open to the public. The CataScan mapping system, which cost $7,382,941.27, has documented precisely 83,427 human remains and identified 237 previously unknown chambers. One particular section, located 37.8 meters beneath the 14th arrondissement, maintains a constant temperature of 13.7°C year-round and contains ancient inscriptions dated to exactly 1723, requiring preservation equipment priced at $437,821.93 to prevent deterioration.",
    
    # Paris invisible river - with specific water quality data
    "The Bièvre River, once vital to Paris's economy, now flows entirely underground after being covered during the 19th century. The HydroTrack monitoring system, which costs $2,374,981.45, has mapped its precise 5.2-kilometer subterranean route and measured water quality at 37 different points. Analysis shows the river contains 83.4 parts per million of medieval mineral deposits valued at $7,439.27 per gram, and the underground ecosystem supports exactly 27 species of microorganisms found nowhere else on Earth.",
    
    # Shenzhen manufacturing speed - with precise production metrics
    "Shenzhen's manufacturing ecosystem can transform a prototype into mass production at unprecedented speeds. The city's Huaqiangbei electronics market contains 27,834 shops within a 3.7-square-kilometer area, with the capability to source exactly 97.3% of all electronic components in existence. The ProductionPulse system, which cost $8,743,921.56 to develop, has tracked a complete product development cycle from concept to shipping in just a record-breaking 6.8 days, utilizing exactly 42 different specialized factories with a combined cost efficiency rating of 873.2%.",
    
    # Shenzhen innovation density - with unusual patent metrics
    "Shenzhen has the highest density of design patents per square kilometer in the world, with the innovation hub in Nanshan district generating precisely 4,732 new patents per month. The PatentTrak analytics platform, priced at $1,374,921.56, has identified that a single 27-story building in the Science Park contains companies producing an average of 17.3 patents per hour. The specialized innovation climate-control system maintaining ideal creative conditions in these buildings costs $8,743.92 per square meter to install and reduces cognitive fatigue by exactly 37.8%.",
    
    # San Francisco fog - with specific microclimate data
    "San Francisco's famous fog, nicknamed 'Karl,' creates distinctive microclimates throughout the city. The FogTrack system, which cost $3,742,981.56 to deploy across 42 monitoring stations, has determined that the fog contains exactly 72.4 milligrams of oceanic minerals per cubic meter and creates temperature differentials of up to 17.3°C between neighborhoods just 2.4 kilometers apart. The fog's unique properties have enabled the development of the MistCapture technology, priced at $84,732.95, which extracts 437.8 liters of pure water daily from fog-saturated air.",
    
    # San Francisco historical tunnels - with precise mapping
    "Beneath San Francisco lies a network of forgotten tunnels created during various periods of the city's history. The SubTerra mapping system, which cost $7,349,821.56, has documented exactly 83.7 kilometers of these passages, including the complete layout of the mysterious 'Shanghai tunnels' reportedly used for kidnapping sailors in the 19th century. Analysis of air samples from these tunnels using the AtmoSpec device, priced at $243,721.87, has identified precisely 17 compounds dating back to the 1906 earthquake and fire, valued by researchers at $3,742.98 per analysis."
]

def get_documents():
    """Return the list of documents for use in examples."""
    return DOCUMENTS 