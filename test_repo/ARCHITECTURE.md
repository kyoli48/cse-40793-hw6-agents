# Pricing application architecture
## A001 Domain purity
Files in domain/ perform calculations only. They must not call print(), perform
network or filesystem I/O, or import ui/.
## A002 Presentation boundary
Only ui/ may display results. ui/ may import domain/.
