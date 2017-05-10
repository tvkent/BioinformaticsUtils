# BioinformaticsUtils
general scripts for bioinformatics

### Modular VCF genotype parsing
Scripts:
- `pull_vcf_samples.awk` takes a header-less VCF and returns only chr,pos,ref,alt,samples columns
- `genotype_vcf_samples.awk` takes output from `pull_vcf_samples.awk` and returns 012 genotype calls
- `get_vcf_genotypes.sh` runs pipeline to get 012 genotypes from VCF. Run with bash `get_vcf_genotypes.sh` vcf output
