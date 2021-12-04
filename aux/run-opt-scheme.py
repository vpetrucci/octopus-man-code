import os
import itertools
import random
import time

all_benchs = [
"libquantum-1397.ref.pfm.50.txt",
"lbm-reference.dat.ref.pfm.50.txt",
"soplex-ref.mps.ref.pfm.50.txt",
"milc-su3imp.in.ref.pfm.50.txt",
"wrf-.ref.pfm.50.txt",
"gcc-g23.i.ref.pfm.50.txt",
"astar-BigLakes2048.cfg.ref.pfm.50.txt",
"gcc-166.i.ref.pfm.50.txt",
"gobmk-score2.tst.ref.pfm.50.txt",
"astar-rivers.cfg.ref.pfm.50.txt",
"gcc-s04.i.ref.pfm.50.txt",
"gobmk-trevorc.tst.ref.pfm.50.txt",
"sjeng-ref.txt.ref.pfm.50.txt",
"omnetpp-omnetpp.ini.ref.pfm.50.txt",
"gobmk-13x13.tst.ref.pfm.50.txt",
"gobmk-trevord.tst.ref.pfm.50.txt",
"gobmk-nngs.tst.ref.pfm.50.txt",
"gcc-200.i.ref.pfm.50.txt",
"h264ref-foreman_ref_encoder_main.cfg.ref.pfm.50.txt",
"bzip2-input.program.ref.pfm.50.txt",
"gcc-expr2.i.ref.pfm.50.txt",
"bzip2-input.source.ref.pfm.50.txt",
"gcc-cp-decl.i.ref.pfm.50.txt",
"h264ref-sss_encoder_main.cfg.ref.pfm.50.txt",
"cactusADM-benchADM.ref.pfm.50.txt",
"gcc-expr.i.ref.pfm.50.txt",
"hmmer-retro.hmm.ref.pfm.50.txt",
"bzip2-input.combined.ref.pfm.50.txt",
"gcc-c-typeck.i.ref.pfm.50.txt",
"gcc-scilab.i.ref.pfm.50.txt",
"bzip2-text.html.ref.pfm.50.txt",
"h264ref-foreman_ref_encoder_baseline.cfg.ref.pfm.50.txt",
"GemsFDTD-ref.ref.pfm.50.txt",
"mcf-inp.in.ref.pfm.50.txt",
"hmmer-nph3.hmm.ref.pfm.50.txt",
"tonto-.ref.pfm.50.txt",
"namd-.ref.pfm.50.txt",
"sphinx3-args.an4.ref.pfm.50.txt",
"gromacs-.ref.pfm.50.txt",
"povray-SPEC-benchmark-ref.ref.pfm.50.txt",
"bwaves-.ref.pfm.50.txt",
"bzip2-chicken.jpg.ref.pfm.50.txt",
"gamess-triazolium.ref.pfm.50.txt",
"bzip2-liberty.jpg.ref.pfm.50.txt",
"leslie3d-.ref.pfm.50.txt",
"zeusmp-.ref.pfm.50.txt",
"gamess-cytosine.2.ref.pfm.50.txt",
"calculix-hyperviscoplastic.ref.pfm.50.txt",
"gamess-h2ocu2+.gradient.ref.pfm.50.txt"]

app_info = {"libquantum-1397.ref.pfm.50.txt":(1.18772710341,1840.23474639),
"lbm-reference.dat.ref.pfm.50.txt":(1.52910996698,2456.21595356),
"soplex-ref.mps.ref.pfm.50.txt":(1.74055433952,719.589670402),
"milc-su3imp.in.ref.pfm.50.txt":(1.75745766861,2071.04042633),
"wrf-.ref.pfm.50.txt":(1.79443004269,0.871651922289),
"gcc-g23.i.ref.pfm.50.txt":(1.79817447192,274.710285126),
"astar-BigLakes2048.cfg.ref.pfm.50.txt":(1.90386697233,896.235433125),
"gcc-166.i.ref.pfm.50.txt":(2.06980748782,136.157614048),
"gobmk-score2.tst.ref.pfm.50.txt":(2.12389354742,406.887097635),
"astar-rivers.cfg.ref.pfm.50.txt":(2.19898294824,1287.80477383),
"gcc-s04.i.ref.pfm.50.txt":(2.20278690441,277.801112833),
"gobmk-trevorc.tst.ref.pfm.50.txt":(2.25017379047,314.262447324),
"sjeng-ref.txt.ref.pfm.50.txt":(2.27066716168,2581.18841258),
"omnetpp-omnetpp.ini.ref.pfm.50.txt":(2.27805104533,2073.70945862),
"gobmk-13x13.tst.ref.pfm.50.txt":(2.28137510043,315.157945394),
"gobmk-trevord.tst.ref.pfm.50.txt":(2.2923880856,435.202310417),
"gobmk-nngs.tst.ref.pfm.50.txt":(2.31409772151,819.738444926),
"gcc-200.i.ref.pfm.50.txt":(2.33779480012,226.245074809),
"h264ref-foreman_ref_encoder_main.cfg.ref.pfm.50.txt":(2.35846614473,315.953130052),
"bzip2-input.program.ref.pfm.50.txt":(2.39009463673,525.169496258),
"gcc-expr2.i.ref.pfm.50.txt":(2.39487404213,246.268312433),
"bzip2-input.source.ref.pfm.50.txt":(2.41625784773,503.341145288),
"gcc-cp-decl.i.ref.pfm.50.txt":(2.42496830549,153.024912856),
"h264ref-sss_encoder_main.cfg.ref.pfm.50.txt":(2.43320919185,2934.3512423),
"cactusADM-benchADM.ref.pfm.50.txt":(2.49170681,6560.44368463),
"gcc-expr.i.ref.pfm.50.txt":(2.49373800159,179.924457952),
"hmmer-retro.hmm.ref.pfm.50.txt":(2.50032349896,1487.32393381),
"bzip2-input.combined.ref.pfm.50.txt":(2.50976470285,408.241287119),
"gcc-c-typeck.i.ref.pfm.50.txt":(2.54096552394,221.735713198),
"gcc-scilab.i.ref.pfm.50.txt":(2.54250634386,84.6756240181),
"bzip2-text.html.ref.pfm.50.txt":(2.61824970432,653.341647651),
"h264ref-foreman_ref_encoder_baseline.cfg.ref.pfm.50.txt":(2.62208366966,410.979095415),
"GemsFDTD-ref.ref.pfm.50.txt":(2.76073226405,4061.20534575),
"mcf-inp.in.ref.pfm.50.txt":(2.76284324883,2811.94502589),
"hmmer-nph3.hmm.ref.pfm.50.txt":(2.84654263159,786.416318614),
"tonto-.ref.pfm.50.txt":(2.86722664962,3174.23305736),
"namd-.ref.pfm.50.txt":(2.92400654945,2774.58715883),
"sphinx3-args.an4.ref.pfm.50.txt":(2.94454502573,5436.38653568),
"gromacs-.ref.pfm.50.txt":(2.96332706614,3218.53606367),
"povray-SPEC-benchmark-ref.ref.pfm.50.txt":(3.01657572948,1340.53961666),
"bwaves-.ref.pfm.50.txt":(3.06281621562,4529.66097249),
"bzip2-chicken.jpg.ref.pfm.50.txt":(3.09716904356,229.275261749),
"gamess-triazolium.ref.pfm.50.txt":(3.25194990634,4648.3533564),
"bzip2-liberty.jpg.ref.pfm.50.txt":(3.47166457819,480.911652848),
"leslie3d-.ref.pfm.50.txt":(3.48711245407,4212.13039009),
"zeusmp-.ref.pfm.50.txt":(3.53389718181,4169.84826748),
"gamess-cytosine.2.ref.pfm.50.txt":(3.59891904106,1362.82862345),
"calculix-hyperviscoplastic.ref.pfm.50.txt":(3.82145123586,7219.26060929),
"gamess-h2ocu2+.gradient.ref.pfm.50.txt":(4.14237215463,1099.90779041)}

app_list_AB = [(('soplex-ref.mps.ref.pfm.50.txt_1','soplex-ref.mps.ref.pfm.50.txt_2','soplex-ref.mps.ref.pfm.50.txt_3','gamess-h2ocu2+.gradient.ref.pfm.50.txt'),'A1'),
            (('milc-su3imp.in.ref.pfm.50.txt_1','milc-su3imp.in.ref.pfm.50.txt_2','milc-su3imp.in.ref.pfm.50.txt_3','zeusmp-.ref.pfm.50.txt'),'A2'),
            (('astar-BigLakes2048.cfg.ref.pfm.50.txt_1','astar-BigLakes2048.cfg.ref.pfm.50.txt_2','astar-BigLakes2048.cfg.ref.pfm.50.txt_3','calculix-hyperviscoplastic.ref.pfm.50.txt'),'A3'),
            (('lbm-reference.dat.ref.pfm.50.txt_1','lbm-reference.dat.ref.pfm.50.txt_2','lbm-reference.dat.ref.pfm.50.txt_3','bwaves-.ref.pfm.50.txt'),'A4'),                        
            (('omnetpp-omnetpp.ini.ref.pfm.50.txt_1','omnetpp-omnetpp.ini.ref.pfm.50.txt_2','omnetpp-omnetpp.ini.ref.pfm.50.txt_3','gobmk-nngs.tst.ref.pfm.50.txt'),'B1'),               
            (('bzip2-input.source.ref.pfm.50.txt_1','bzip2-input.source.ref.pfm.50.txt_2','bzip2-input.source.ref.pfm.50.txt_3','cactusADM-benchADM.ref.pfm.50.txt'),'B2'),               
            (('mcf-inp.in.ref.pfm.50.txt_1','mcf-inp.in.ref.pfm.50.txt_2','mcf-inp.in.ref.pfm.50.txt_3','namd-.ref.pfm.50.txt'),'B3'),
            (('GemsFDTD-ref.ref.pfm.50.txt_1','GemsFDTD-ref.ref.pfm.50.txt_2','GemsFDTD-ref.ref.pfm.50.txt_3','sphinx3-args.an4.ref.pfm.50.txt'),'B4')]


app_list_16 = ['soplex-ref.mps.ref.pfm.50.txt',
            'gamess-h2ocu2+.gradient.ref.pfm.50.txt',
            'milc-su3imp.in.ref.pfm.50.txt',
            'zeusmp-.ref.pfm.50.txt',
            'astar-BigLakes2048.cfg.ref.pfm.50.txt',
            'calculix-hyperviscoplastic.ref.pfm.50.txt',
            'lbm-reference.dat.ref.pfm.50.txt',
            'bwaves-.ref.pfm.50.txt',
            #'omnetpp-omnetpp.ini.ref.pfm.50.txt',
            'gobmk-nngs.tst.ref.pfm.50.txt',
            'bzip2-input.source.ref.pfm.50.txt',
            'cactusADM-benchADM.ref.pfm.50.txt',
            'mcf-inp.in.ref.pfm.50.txt',
            'namd-.ref.pfm.50.txt',
    #        'sphinx3-args.an4.ref.pfm.50.txt',
            'GemsFDTD-ref.ref.pfm.50.txt',
            'tonto-.ref.pfm.50.txt']

all_comb=[i for i in itertools.combinations(app_list_16, 4)]
all_comb_8=[i for i in itertools.combinations(app_list_16, 8)]

rand_app_list = []
for bla in range(10):
    bench_num = random.randint(0, len(all_comb)-1)
    apps = all_comb[bench_num]
    comp = 'R4-'+str(bench_num)
    rand_app_list += [(apps,comp)]

rand_app_list_8 = []
for bla in range(10):
    bench_num = random.randint(0, len(all_comb_8)-1)
    apps = all_comb_8[bench_num]
    comp = 'R8-'+str(bench_num)
    rand_app_list_8 += [(apps,comp)]

#rand_app_list = [(('gamess-h2ocu2+.gradient.ref.pfm.50.txt', 'bwaves-.ref.pfm.50.txt', 'bzip2-input.source.ref.pfm.50.txt', 'mcf-inp.in.ref.pfm.50.txt'), 'R743'), (('astar-BigLakes2048.cfg.ref.pfm.50.txt', 'cactusADM-benchADM.ref.pfm.50.txt', 'namd-.ref.pfm.50.txt', 'tonto-.ref.pfm.50.txt'), 'R1476'), (('gamess-h2ocu2+.gradient.ref.pfm.50.txt', 'zeusmp-.ref.pfm.50.txt', 'mcf-inp.in.ref.pfm.50.txt', 'namd-.ref.pfm.50.txt'), 'R589'), (('gamess-h2ocu2+.gradient.ref.pfm.50.txt', 'astar-BigLakes2048.cfg.ref.pfm.50.txt', 'calculix-hyperviscoplastic.ref.pfm.50.txt', 'bwaves-.ref.pfm.50.txt'), 'R600'), (('soplex-ref.mps.ref.pfm.50.txt', 'astar-BigLakes2048.cfg.ref.pfm.50.txt', 'namd-.ref.pfm.50.txt', 'GemsFDTD-ref.ref.pfm.50.txt'), 'R285'), (('soplex-ref.mps.ref.pfm.50.txt', 'astar-BigLakes2048.cfg.ref.pfm.50.txt', 'bwaves-.ref.pfm.50.txt', 'GemsFDTD-ref.ref.pfm.50.txt'), 'R260'), (('gamess-h2ocu2+.gradient.ref.pfm.50.txt', 'lbm-reference.dat.ref.pfm.50.txt', 'cactusADM-benchADM.ref.pfm.50.txt', 'mcf-inp.in.ref.pfm.50.txt'), 'R720'), (('milc-su3imp.in.ref.pfm.50.txt', 'calculix-hyperviscoplastic.ref.pfm.50.txt', 'GemsFDTD-ref.ref.pfm.50.txt', 'tonto-.ref.pfm.50.txt'), 'R1104'), (('lbm-reference.dat.ref.pfm.50.txt', 'gobmk-nngs.tst.ref.pfm.50.txt', 'astar-BigLakes2048.cfg.ref.pfm.50.txt', 'GemsFDTD-ref.ref.pfm.50.txt'), 'R1656'), (('bwaves-.ref.pfm.50.txt', 'gobmk-nngs.tst.ref.pfm.50.txt', 'bzip2-input.source.ref.pfm.50.txt', 'tonto-.ref.pfm.50.txt'), 'R1699'), (('soplex-ref.mps.ref.pfm.50.txt', 'calculix-hyperviscoplastic.ref.pfm.50.txt', 'gobmk-nngs.tst.ref.pfm.50.txt', 'bzip2-input.source.ref.pfm.50.txt'), 'R307'), (('gamess-h2ocu2+.gradient.ref.pfm.50.txt', 'calculix-hyperviscoplastic.ref.pfm.50.txt', 'namd-.ref.pfm.50.txt', 'GemsFDTD-ref.ref.pfm.50.txt'), 'R694'), (('lbm-reference.dat.ref.pfm.50.txt', 'bwaves-.ref.pfm.50.txt', 'cactusADM-benchADM.ref.pfm.50.txt', 'namd-.ref.pfm.50.txt'), 'R1624'), (('soplex-ref.mps.ref.pfm.50.txt', 'zeusmp-.ref.pfm.50.txt', 'lbm-reference.dat.ref.pfm.50.txt', 'astar-BigLakes2048.cfg.ref.pfm.50.txt'), 'R196'), (('gamess-h2ocu2+.gradient.ref.pfm.50.txt', 'astar-BigLakes2048.cfg.ref.pfm.50.txt', 'bzip2-input.source.ref.pfm.50.txt', 'tonto-.ref.pfm.50.txt'), 'R638'), (('milc-su3imp.in.ref.pfm.50.txt', 'zeusmp-.ref.pfm.50.txt', 'lbm-reference.dat.ref.pfm.50.txt', 'tonto-.ref.pfm.50.txt'), 'R848'), (('milc-su3imp.in.ref.pfm.50.txt', 'gobmk-nngs.tst.ref.pfm.50.txt', 'namd-.ref.pfm.50.txt', 'tonto-.ref.pfm.50.txt'), 'R1066'), (('milc-su3imp.in.ref.pfm.50.txt', 'astar-BigLakes2048.cfg.ref.pfm.50.txt', 'namd-.ref.pfm.50.txt', 'GemsFDTD-ref.ref.pfm.50.txt'), 'R935'), (('gamess-h2ocu2+.gradient.ref.pfm.50.txt', 'milc-su3imp.in.ref.pfm.50.txt', 'calculix-hyperviscoplastic.ref.pfm.50.txt', 'bwaves-.ref.pfm.50.txt'), 'R479'), (('zeusmp-.ref.pfm.50.txt', 'calculix-hyperviscoplastic.ref.pfm.50.txt', 'GemsFDTD-ref.ref.pfm.50.txt', 'tonto-.ref.pfm.50.txt'), 'R1204')]


for apps, comb in app_list_AB:
#for apps, comb in rand_app_list_8:
    print 'running', apps, 'with Linux scheduling'
    os.system("python opt-scheme4.py 0 " + str(apps)[1:-1].replace(",",'').replace("'",''))
    os.system('mv mapping-o0.txt mapping-o0-'+comb+'.txt')
    os.system('mv power-o0.txt power-o0-'+comb+'.txt')    
    os.system('mv times.0.txt times.0-'+comb+'.txt')
    os.system('mv opt-time.pkl opt-time-'+comb+'.pkl')

    time.sleep(5)
 
    print 'running', apps, 'with Opt-Scheme scheduling'
    os.system("python opt-scheme4.py 1 " + str(apps)[1:-1].replace(",",'').replace("'",''))
    os.system('mv mapping-o1.txt mapping-o1-'+comb+'.txt')
    os.system('mv power-o1.txt power-o1-'+comb+'.txt')    
    os.system('mv times.1.txt times.1-'+comb+'.txt')
    os.system('mv opt-time.pkl opt-time-'+comb+'.pkl')
    
    time.sleep(5)

