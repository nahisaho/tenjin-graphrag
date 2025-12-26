# Education Theories Sample Data

This directory contains sample data for the TENGIN Education Theory GraphRAG system.

## Data Files

- `theories.json` - Education theory definitions
- `theorists.json` - Theorist (educator) information  
- `concepts.json` - Key educational concepts
- `principles.json` - Practical principles derived from theories
- `evidence.json` - Research evidence supporting theories
- `relationships.json` - Graph relationships between entities

## Data Structure

### Theory Categories
- `learning` - Learning theories
- `instructional` - Instructional design theories
- `developmental` - Developmental psychology theories
- `motivation` - Motivation theories
- `edtech` - Educational technology theories

### Evidence Levels
- `strong` - Meta-analyses, multiple RCTs
- `moderate` - Single RCT, multiple quasi-experiments
- `limited` - Single quasi-experiment
- `theoretical` - Theoretical framework only
- `emerging` - New research area

## Loading Data

Use the seed script to load data into Neo4j:

```bash
uv run python -m tengin_mcp.scripts.seed_data
```
