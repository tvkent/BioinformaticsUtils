BEGIN{OFS="\t"; hrsum=0; hasum=0; thsum=0; hetsum=0}
{
	hrsum+=$3
	hasum+=$4
	thsum+=$5
	hetsum+=$6

	print $1,$2,hrsum,hasum,thsum,hetsum,$7,$8
}
