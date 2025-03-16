## Adversarial Code Generation Using Reasoning Models

### Running the system
To reproduce our results:
```
pip install -r requirements.txt
python main.py
```
### Our results
We ran this multi-agent system for the following configurations:
- G (baseline): A generator/coder agent
- GC: A generator and critic agent
- GCD: A generator, critig and debugger agent
- PGC: A planner, generator and critic agent
- PGCD A planner, generator, critic and debugger agent

Output and evaluated output can be found in `results/`
