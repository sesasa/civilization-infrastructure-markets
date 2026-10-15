from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch,FancyArrowPatch
R=Path(__file__).parent
plt.rcParams.update({'font.family':'DejaVu Sans','text.color':'#173648'})
fig,ax=plt.subplots(figsize=(11,5.6));ax.set_xlim(0,11);ax.set_ylim(0,5.6);ax.axis('off')
ax.text(.25,5.22,'From added capacity to functioning systems',fontsize=19,weight='bold')
ax.text(.25,4.88,'A functional analogy — not an embryonic age or a biological forecast',fontsize=10,color='#5c7080')
xs=[.3,3.9,7.5];w=3.15;h=.95
labels=[['Maternal resource exchange','Vessels and tissue supply','Specialized developing tissues'],['Energy, water and materials','Grids, cooling and local delivery','Compute, factories and services']]
for y,row,col in [(3.15,labels[0],'#e5edf8'),(1.15,labels[1],'#e2f0e9')]:
 for x,t in zip(xs,row):
  ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.04,rounding_size=.12',facecolor=col,edgecolor='#8ba1ad',lw=.7))
  import textwrap
  ax.text(x+w/2,y+h/2,'\n'.join(textwrap.wrap(t,28)),ha='center',va='center',fontsize=10.5)
 for x in xs[:2]:ax.add_patch(FancyArrowPatch((x+w+.06,y+h/2),(x+3.6-.07,y+h/2),arrowstyle='-|>',mutation_scale=13,color='#35536a'))
ax.text(.3,4.35,'DEVELOPMENTAL BIOLOGY',fontsize=9.5,weight='bold',color='#425879')
ax.text(.3,2.35,'CIVILIZATION: INFERRED PARALLEL',fontsize=9.5,weight='bold',color='#306247')
for y in [2.89,.88]:
 ax.add_patch(FancyArrowPatch((9.7,y),(1.15,y),arrowstyle='-|>',mutation_scale=13,connectionstyle='arc3,rad=-.07',color='#a06635',lw=1.4))
ax.text(5.4,2.48,'Local signals and flow reshape supply and structure',ha='center',fontsize=9,color='#8b5b31')
ax.text(5.4,.47,'Telemetry, prices, contracts and outcomes reshape investment',ha='center',fontsize=9,color='#8b5b31')
ax.text(.3,.09,'The engineering task is reliable interaction: more connection is useful only when feedback and failure behavior work.',fontsize=9)
fig.tight_layout(pad=.3);fig.savefig(R/'development_function_map.png',dpi=180);fig.savefig(R/'development_function_map.svg');plt.close(fig)
