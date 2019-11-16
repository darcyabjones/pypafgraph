# pypafgraph

Scripts to support the fungraph pipeline.
Mostly this is to reduce complexity of alignments before inducing a pan-genome graph using seqwish.

- Extract repeat regions given a soft-masked fasta file.
- Finding duplicated regions given self aligned genomes.
- Filtering minimap2 PAF alignments based on alignment length and intersection with repetitive content.
- Performing clustering of all-vs-all alignments to select components for alignment.

Removing alignments between sequences that are exclusively within repeat regions really helps to avoid hairballs that fail to discriminate separate chromosomes.
Similarly, extracting connected subgraphs given a coarse alignment/harsher filtering setting and processing the components individually using more relaxed parameters seems to give a good balance between representing reality and interpretability.

The clustering uses an MCL algorithm with relaxed parameters.
Connected components would also work, but requires pre-filtering of the alignments based on large minimum alignment length to avoid merging unrelated components by a stray connection.
The MCL should, in theory, be able to recognise that the few edges connecting otherwise unconnected components should be disregarded.
Another algorithm to try in the future would be affinity propagation.

Edges and edge weights for the MCL are determined from the pair-wise minimap2 alignments and alignment coverage of the shorter sequence $ alilen / min(qlen, tlen) $.

This is a work in progress.
