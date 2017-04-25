import sys
sys.path.append("refine.py")
import refine

r = refine.Refine()
p = r.new_project("all_samples.tsv")
p.apply_operations("operations.json")
print p.export_rows()
p.delete_project()
