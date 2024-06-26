# Copyright 2005 - 2015 Harri Pitkänen (hatapitk@iki.fi)
# Functions and data for Joukahainen -> Suomi-malaga converter

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


# Hannu Väisänen has added some inflection types.

import re

grads = [ ('sw', 'tt', 'av1'),
	('sw', 'pp', 'av1'),
	('sw', 'kk', 'av1'),
	('sw', 'mp', 'av1'),
	('sw', 'p', 'av1'),
	('sw', 'nt', 'av1'),
	('sw', 'lt', 'av1'),
	('sw', 'rt', 'av1'),
	('sw', 't', 'av1'),
	('sw', 'nk', 'av1'),
	('sw', 'uku', 'av1'),
	('sw', 'yky', 'av1'),
	('ws', 'b', 'av2'),
	('ws', 'g', 'av2'),
	('ws', 't', 'av2'),
	('ws', 'p', 'av2'),
	('ws', 'k', 'av2'),
	('ws', 'mm', 'av2'),
	('ws', 'v', 'av2'),
	('ws', 'nn', 'av2'),
	('ws', 'll', 'av2'),
	('ws', 'rr', 'av2'),
	('ws', 'd', 'av2'),
	('ws', 'ng', 'av2'),
	('sw', 'k>j', 'av3'),
	('ws', 'j>k', 'av4'),
	('sw', 'k>', 'av5'),
	('ws', '>k', 'av6')   ]

# Joukahainen word classes
SUBST = 1
ADJ = 2
VERB = 3

modern_classmap = [('valo', 'sw', [(None,'(.*)','valo'),
			('k>','(ko)ko','koko'),
			('k>','(.*uo)ko','ruoko'),
			('kk','(.*k)kU','alku'),
			('uku','(.*U)kU','luku'),
			('k>','(..U)kU','tiuku'),
			('k>','(.*)kU','alku'),
			('lt','(.*l)tO','aalto'),
			('nt','(.*n)tO','anto'),
			('nt','(.*n)tU','lintu'),
			('nk','(.*n)kO','hanko'),
			('tt','(.*t)tU','hattu'),
			('tt','(.*t)tO','liitto'),
			('nk','(.*n)kU','hinku'),
			('pp','(.*p)pU','hoppu'),
			('rt','(.*r)tO','kaarto'),
			('pp','(.*p)pO','kippo'),
			('mp','(.*m)pO','sampo'),
			('mp','(.*m)pU','kumpu'),
			('t','(.*)tU','laatu'),
			('p','(.*)pU','apu'),
			('p','(.*)pO','lepo'),
			('t','(.*)tO','leuto'),
			('kk','(.*k)kO','verkko'),
			('k>','(.*h)kO','vihko'),
			('k>','(.*)kO','verkko')   ]),
	('arvelu', 'sw', [(None,'(.*Ce[lr])O','hontelo',[ADJ]),
			(None,'(.*)','arvelu'),
			('nk','(.*n)kO','alanko'),
			('nt','(.*n)tO','avanto'),
			('kk','(.*k)kO','laatikko'),
			('tt','(.*t)tO','pihatto'),
			('tt','(.*t)tU','raamattu') ]),
	('autio', '-', [(None,'(.*)','autio')]),
	('kiiski', '-', [(None,'(.*)i','kiiski')]),
	('siisti', '-', [(None,'(.*)i','siisti')]),
	('risti', 'sw', [(None,'(.*)i','risti'),
			('pp','(pop)pi','pop'),
			('pp','(.*p)pi','keppi'),
			('lt','(.*l)ti','pelti'),
			('nk','(.*n)ki','renki'),
			('kk','(punk)ki','punk'),
			('kk','(.*k)ki','takki'),
			('tt','(.*t)ti','tatti'),
			('nt','(.*n)ti','tunti'),
			('p','(.*)pi','hupi'),
			('t','(.*)ti','vati'),
			('k>','(.*)ki','takki')]),
	('paperi', 'sw', [(None,'(.*)i','paperi'),
			('nt','(.*n)ti','hollanti'),
			('nk','(.*n)ki','killinki'),
			('kk','(.*k)ki','kajakki'),
			('tt','(.*t)ti','salaatti'),
			('pp','(.*p)pi','sinappi'),
			('t','(.*)ti','konvehti') ]),
	('edam', '-', [(None,'(.*C)','edam')]),
	('kalsium', '-', [(None,'(.*)i','fan'),
			 (None,'(.*)','kalsium')]),
	('lovi', 'sw',   [(None,'(.*)i','lovi'),
			('nk','(.*n)ki','hanki'),
			('pp','(.*p)pi','happi'),
			('mp','(.*lam)pi','lampi'),
			('mp','(.*m)pi','sampi'),
			('kk','(.*k)ki','kaikki'),
			('k>j','(.*)ki','kylki'),
			('t','(.*lah)ti','lahti'),
			('t','(.*h)ti','lehti'),
			('p','(.*)pi','siipi'),
			('k>','(.*i)ki','piki'),
			('k>','(.*)ki','kaikki')]),
	('toholampi', '-', [(None,'(.*lam)pi','toholampi')]),
	('suksi', '-', [(None,'(.*u)ksi','suksi')]),
	('veli', '-', [(None,'(.*el)i','veli')]),
	('nalle', 'sw', [(None,'(.*Ce)','nalle'),
			 (None,'(.*Cé)','nalle'),
		         (None,'(.*[iu]e)','nalle'),
		         ('tt','(.*t)te','atte'),
		         ('pp','(.*p)pe','hjerppe'),
		         ('kk','(.*k)ke','nukke')]),
	('kala', 'sw',   [(None,'(.*)A','kala'),
			('tt','(.*t)tA','aitta'),
			('nk','(.*n)kA','hanka'),
			('mp','(.*m)pA','kampa'),
			('nt','(.*n)tA','kanta'),
			('pp','(.*p)pA','kappa'),
			('rt','(.*r)tA','parta'),
			('lt','(.*l)tA','valta'),
			('kk','(.*k)kA','haka'),
			('p','(.*)pA','napa'),
			('t','(.*)tA','pata'),
			('k>j','(.*A)ikA','aika'),
			('k>','(.*AA)kA','raaka'),
			('k>','(.*V)kA','liika'),
			('k>','(.*C)kA','haka')]),
	('nahka', '-', [(None,'(.*)kA','nahka')]),
	('jumala', '-', [(None,'(.*l)A','jumala')]),
	('koira', 'sw',   [(None,'(.*)A','koira'),
			('tt','(.*t)tA','kenttä'),
			('nk','(.*n)kA','honka'),
			('mp','(.*m)pA','kompa'),
			('nt','(.*n)tA','suunta'),
			('pp','(.*p)pA','tolppa'),
			('rt','(.*r)tA','turta'),
			('lt','(.*l)tA','kulta'),
			('kk','(.*k)kA','hoikka'),
			('p','(.*)pA','huopa'),
			('t','(.*)tA','juhta'),
			('k>','(.*i)kA','ikä'),
			('k>','(.*)kA','hoikka')]),
	('ylkä', '-', [(None,'(.*l)kA','ylkä')]),
	('pitkä', '-', [(None,'(.*pi)tkA','pitkä')]),
	('ruoka', '-', [(None,'(.*ru)oka','ruoka')]),
	('poika', '-', [(None,'(.*po)ikA','poika')]),
	('matala', '-', [(None,'(.*C)A','matala')]),
	('asema', 'sw',  [(None,'(.*)A','asema'),
			('tt','(.*t)tA','opotta'),
			('nt','(.*n)tA','emäntä')]),
	('kulkija', '-', [(None,'(.*i)jA','kulkija'),
			(None,'(.*)A','apila')]),
	('video', '-', [(None,'(.*deO)','video')]),
	('karahka', 'sw', [(None,'(.*)A','karahka'),
			('tt','(.*t)tA','savotta'),
			('pp','(.*p)pA','ulappa'),
			('kk','(.*k)kA','solakka'),
		        ('nt','(.*n)tA','veranta')]),
	('apaja', '-', [(None,'(.*C)A','apaja')]),
	('peruna', '-', [(None,'(.*C)A','peruna')]),
	('korkea', '-', [(None,'(.*C)eA','korkea'),
		         (None,'(.*O)A','ainoa')]),
	('suurempi', 'sw', [('mp','(.*V)mpi','suurempi')]),
	('vapaa', '-', [(None,'(.*CA)A','vapaa'),
		        (None,'(.*CO)O','tienoo'),
		        (None,'(.*CU)U','leikkuu')]),
	('kamee', '-',   [(None,'(.*Ce)e','kamee'),
			(None,'(.*CA)A','nugaa'),
			(None,'(.*CO)O','trikoo'),
			(None,'(.*CU)U','revyy')]),
	('pii', '-', [(None,'(.*V)i','pii'),
		      (None,'(.*A)A','maa'),
		      (None,'(.*Ce)e','tee'),
		      (None,'(.*U)U','puu')]),
	('suo', '-', [(None,'(.*C)UO','suo')]),
	('askel', 'ws', [(None,'(.*VC)','askel'),
		         ('nn','(.*n)nel','kannel'),
		         ('nn','(.*n)ner','kinner'),
		         ('nn','(.*n)nAr','piennar'),
		         ('mm','(.*m)mel','ommel'),
		         ('ng','(.*n)ger','penger'),
		         ('d','(.*)dAr','udar'),
		         ('v','(.*)vAl','taival'),
		         ('>k','(.*)en','säen')]),
	('rosé', '-', [(None,'(.*V)','rosé')]),
	('spray', '-', [(None,'(.*[ao]y)','spray')]),
	('parfait', '-', [(None,'(.*)','parfait')]),
	('huuli', '-', [(None,'(.*C)i','tuohi')]),
	('meri', '-', [(None,'(.*er)i','meri')]),
	('tuohi', '-', [(None,'(.*C)i','lohi')]),
	('niemi', '-', [(None,'(.*V)mi','niemi')]),
	('pieni', '-', [(None,'(.*n)i','pieni')]),
	('lumi', '-', [(None,'(.*V)mi','lumi')]),
	('susi', '-', [(None,'(.*V)si','susi')]),
	('tosi', '-', [(None,'(.*V)si','tosi')]),
	('kansi', '-', [(None,'(.*n)si','kansi'),
	                  (None,'(.*r)si','hirsi'),
		        (None,'(.*l)si','jälsi')]),
	('sisar', 'ws', [(None,'(.*CVC)','sisar'),
		         ('t','(.*t)Ar','tytär'),
		         ('>k','(.*i)en','ien')]),
	('hapan', '-', [(None,'(.*p)An','hapan')]),
	('uistin', 'ws', [(None,'(.*[iaä])n','uistin'),
	                    ('nn','(.*n)nin','vaimennin'),
		          ('ll','(.*l)lin','sivellin'),
		          ('rr','(.*r)rin','kiharrin'),
		          ('rr','(.*r)rOin','kerroin'),
		          ('d','(.*)din','kaadin'),
		          ('v','(.*)vin','kaavin'),
			  ('t','(.*t)in','suodatin'),
			  ('k','(.*k)in','puin'),
		          ('j>k','(.*l)jin','poljin'),
		          ('>k','(.*)in','puin')]),
	('laidun', '-', [(None,'(.*)dUn','laidun')]),
	('onneton', 'ws', [(None,'(.*t)On','alaston'),
	                     ('t','(.*t)On','onneton')]),
	('lämmin', '-', [(None,'(.*m)min','lämmin')]),
	('vasen', '-', [(None,'(.*e)n','vasen')]),
	('sisin', '', [(None,'(.*)in','pahin')]),
	('nainen', '-', [(None,'(.*)nen','nainen')]),
	('vastaus', '-', [(None,'(.*V)s','vastaus')]),
	('kalleus', '-', [(None,'(.*VU)s','kalleus'),
	                    (None,'(.*vU)s','kalleus')]),
	('kaunis', '-', [(None,'(.*C)is','kaunis')]),
	('autuas', '-', [(None,'(.*U)As','autuas')]),
	('laupias', '-', [(None,'(.*p)iAs','laupias')]),
	('vieras', 'ws', [(None,'(.*[lmr]i[aä])s','antelias'),
		            (None,'(.*il[aä])s','antelias'),
		            (None,'(.*A)s','vieras'),
	                    (None,'(.*)is','kauris'),
			(None,'(.*e)s','kirves'),
	                    ('nn','(.*n)nAs','kinnas'),
		          ('ll','(.*l)lAs','allas'),
		          ('rr','(.*r)rAs','harras'),
		          ('mm','(.*m)mAs','hammas'),
		          ('ng','(.*n)gAs','kangas'),
			('k','(.*k)As','avokas',[SUBST]),
			('k','(.*k)As','vilkas',[ADJ]),
		          ('p','(.*p)As','saapas'),
		          ('d','(.*)dAs','ahdas'),
		          ('v','(.*)vAs','varvas'),
		          ('t','(.*t)As','ratas'),
			('t','(.*t)is','altis'),
		          ('>k','(.*)As','varas'),
			('>k','(.*)is','ruis'),
			('>k','(.*)es','ies')]),
	('iäkäs', 'ws', [('k','(.*k)As','iäkäs',[ADJ]),
		         ('k','(.*k)As','asiakas',[SUBST])]),
	('ohut', '-', [(None,'(.*CU)t','airut')]),
	('kevät', '-', [(None,'(.*A)t','kevät')]),
	('mies', '-', [(None,'(.*mie)s','mies')]),
	('kuollut', '-', [(None,'(.*C)Ut','kuollut')]),
	('hame', 'ws', [(None,'(.*e)','hame'),
	                  ('nn','(.*n)ne','enne'),
		        ('ll','(.*l)le','helle'),
		        ('rr','(.*r)re','kierre'),
		        ('mm','(.*m)me','lumme'),
		        ('j>k','(.*C)je','lahje'),
		        ('p','(.*p)e','lape'),
		        ('d','(.*)de','sade'),
		        ('v','(.*)ve','taive'),
		        ('k','(.*k)e','tarvike'),
		        ('>k','(.*V)e','tarvike'),
		        ('>k','(.*h)e','tarvike'),
		        ('t','(.*Vt)e','vaate'),
		        ('t','(.*lt)e','vaate'),
		        ('t','(.*rt)e','vaate')]),
	('alkeet', '-', [(None,'(.*ke)et','alkeet')]),
	('tie', '-', [(None,'(.*t)ie','tie')]),
	('lapsi', '-', [(None,'(.*)psi','lapsi')]),
	('hapsi', '-', [(None,'(.*)psi','hapsi')]),
	('loppu', '-', [(None,'(.*)','loppu')]),
	('veitsi', '-', [(None,'(.*)tsi','veitsi')]),
        ('kantaja', '-', [(None,'(.*j)A', 'kantaja')]), # Historical inflection (Nykysuomen sanakirja, noun type 16).
        ('koiras', '-', [(None,'(.*)s','koiras')]),    # Historical inflection (Nykysuomen sanakirja, noun type 70).
	# Verbs
	('punoa', 'sw', [(None,'(.*)A','punoa'),
	                   ('mp','(.*m)pUA','ampua'),
	                   ('mp','(.*m)pOA','tempoa'),
		         ('tt','(.*t)tUA','asettua'),
		         ('tt','(.*t)tOA','viittoa'),
		         ('kk','(.*k)kOA','aikoa'),
		         ('kk','(.*k)kUA','kiekua'),
		         ('pp','(.*p)pOA','harppoa'),
		         ('pp','(.*p)pUA','kieppua'),
		         ('nt','(.*n)tUA','jakaantua'),
		         ('rt','(.*r)tOA','kertoa'),
		         ('rt','(.*r)tUA','kumartua'),
		         ('nk','(.*n)kUA','mankua'),
		         ('nk','(.*n)kOA','penkoa'),
		         ('lt','(.*l)tUA','paleltua'),
		         ('t','(.*)tUA','kaatua'),
		         ('t','(.*)tOA','tahtoa'),
		         ('p','(.*)pOA','leipoa'),
		         ('p','(.*)pUA','saapua'),
		         ('k>','(.*U)kUA','liukua'),
		         ('k>','(.*)kOA','aikoa'),
		         ('k>','(.*)kUA','kiekua')]),
	('aavistaa', 'sw', [(None,'(.*t)AA','aavistaa'),
	                      ('rt','(.*r)tAA','longertaa'),
	                      ('tt','(.*t)tAA','alittaa'),
			  ('t','(.*h)tAA','astahtaa')]),
	('hidastaa', '-', [(None,'(.*t)AA','hidastaa')]),
	('heittää', 'sw', [('tt','(.*t)tAA','heittää')]),
	('muistaa', '-', [(None,'(.*C)AA','muistaa')]),
	('inttää', 'sw', [('tt','(.*t)tAA','inttää'),
	                    ('t','(.*)tAA','itää')]),
	('sulaa', 'sw', [(None,'(.*C)AA','sulaa'),
	                   ('nt','(.*n)tAA','kyntää1'),
		         ('tt','(.*t)tAA','autioittaa'),
		         ('t','(.*)tAA','kulahtaa'),
		         ('k>','(.*C)kAA','purkaa')]),
	('hohtaa', 'sw', [('tt','(.*t)tAA','jättää'),
	                   ('nt','(.*n)tAA','kyntää2'),
	                    ('t','(.*)tAA','hohtaa')]),
	('hujahtaa', 'sw', [('t','(.*V)htAA','hujahtaa')]),
	('kirjoittaa', 'sw', [('tt','(.*V)ittAA','kirjoittaa'),
			    ('tt','(.*V)ttAA','ammottaa')]),
	('loistaa', '-', [(None,'(.*C)AA','loistaa')]),
	('vuotaa', 'sw', [('lt','(.*Vl)tAA','puoltaa'),
			('rt','(.*Vr)tAA','juurtaa'),
			('nt','(.*Vn)tAA','saksantaa'),
			('t','(.*V)tAA','vuotaa')]),
	('huutaa', 'sw', [('nt','(.*Vn)tAA','alentaa'),
			('t','(.*V)tAA','huutaa')]),
	('sukeltaa', 'sw', [('lt','(.*Vl)tAA','sukeltaa'),
			  ('rt','(.*Vr)tAA','musertaa'),
			  ('nt','(.*Vn)tAA','jäykentää')]),
	('paleltaa', 'sw', [('lt','(.*Vl)tAA','paleltaa'),
			  ('nt','(.*Vn)tAA','nuotintaa')]),
	('murtaa', 'sw', [('rt','(.*Vr)tAA','murtaa')]),
	('juontaa', 'sw', [('nt','(.*Vn)tAA','juontaa'),
			 ('rt','(.*Vr)tAA','pyörtää')]),
	('pahentaa', 'sw', [('nt','(.*Vn)tAA','pahentaa')]),
	('kaivaa', 'sw', [(None,'(.*C)AA','kaivaa'),
	                    ('nt','(.*n)tAA','antaa'),
			('pp','(.*p)pAA','lappaa'),
			('tt','(.*t)tAA','saattaa'),
			('kk','(.*k)kAA','jakaa'),
			('k>','(.*)kAA','jakaa'),
			('t','(.*)tAA','raataa')]),
	('kaikaa', '-', [(None,'(.*C)AA','kapsaa')]),
	('soutaa', 'sw', [('lt','(.*l)tAA','yltää'),
                          ('nt','(.*n)tAA','entää'),
                          ('t','(.*)tAA','soutaa')]),
	('saartaa', '-', [(None,'(.*r)tAA','saartaa')]),
	('laskea', 'sw', [(None,'(.*C)eA','laskea'),
	                    ('nk','(.*n)keA','tunkea'),
			('t','(.*)teA','kutea'),
			('kk','(.*k)keA','hakea'),
			('p','(.*)peA','rypeä'),
			('k>j','(.*)keA','polkea'),
			('k>','(.*)keA','hakea')]),
	('tuntea', 'sw', [('nt','(.*tUn)teA','tuntea')]),
	('lähteä', 'sw', [('t','(.*lA)hteA','lähteä')]),
	('sallia', 'sw', [(None,'(.*C)iA','sallia'),
			('nk','(.*n)kiA','onkia'),
			('mp','(.*m)piA','empiä'),
			('nt','(.*n)tiA','kontia'),
			('pp','(.*p)piA','oppia'),
			('kk','(.*k)kiA','loikkia'),
			('tt','(.*t)tiA','sättiä'),
			('t','(.*)tiA','laatia'),
			('p','(.*)piA','kaapia'),
			('k>j','(.*)kiA','hylkiä'),
			('k>','(.*i)kiA','poikia'),
			('k>','(.*)kiA','loikkia')]),
	('voida', 'ws', [('t','(.*)idA','voida')]),
	('käydä', None, [(None,'(.*)UdA','käydä')]),
	('kanavoida', 'ws', [('t','(.*O)idA','kanavoida')]),
	('saada', '-', [(None,'(.*CA)AdA','saada'),
	                  (None,'(.*CU)UdA','myydä')]),
	('juoda', '-', [(None,'(.*C)UOdA','juoda'),
		        (None,'(.*C)iedA','viedä')]),
	('nuolaista', 'ws', [(None,'(CAis)tA','nousta'),
			   (None,'(.*CA)istA','nuolaista'),
			   (None,'(.*C)istA','kalista'),
			   (None,'(.*s)tA','nousta'),
			   ('v','(.*)vistA','vavista'),
			   ('ng','(.*n)gAistA','rangaista')]),
	('mennä', '-', [(None,'(.*n)nA','mennä')]),
	('purra', '-', [(None,'(.*r)rA','purra')]),
	('katsella', 'ws', [(None,'(.*Ael)lA','arvailla'),
			(None,'(.*el)lA','katsella'),
			(None,'(.*eil)lA','katsella'),
			(None,'(.*Vil)lA','arvailla'),
			(None,'(.*il)lA','katsella'),
			(None,'(.*Ol)lA','tulla'),
			(None,'(.*Ul)lA','tulla'),
			('mm','(.*m)mellA','ommella'),
			('rr','(.*r)rellA','askarrella'),
			('nn','(.*n)nellA','pienennellä'),
			('ll','(.*l)lellA','takellella'),
			('k','(.*k)ellA','nakella'),
			('t','(.*t)ellA','aatella'),
			('p','(.*p)ellA','tapella'),
			('d','(.*)dellA','kohdella'),
			('>k','(.*)ellA','nakella')]),
	('haravoida', 'ws', [('t','(.*O)idA','haravoida')]),
	('valita', '-', [(None,'(.*i)tA','valita')]),
	('saneerata', '-', [(None,'(.*C)AtA','saneerata')]),
	('aleta', 'ws',  [(None,'(.*CV)tA','aleta'),
	                    ('mm','(.*m)metA','lämmetä'),
			('t','(.*t)OtA','loitota'),
			('p','(.*p)AtA','hapata'),
			('p','(.*p)etA','suipeta'),
			('k','(.*k)etA','vaieta'),
			('d','(.*)detA','edetä'),
			('d','(.*)dOtA','leudota'),
			('d','(.*)dAtA','mädätä'),
			('v','(.*)vetA','kaveta'),
			('j>k','(.*)jetA','tarjeta'),
			('>k','(.*)OtA','ulota'),
			('>k','(.*)AtA','erata'),
			('>k','(.*)etA','vaieta')]),
	('haluta', 'ws', [(None,'(.*V)tA','haluta'),
			('ll','(.*l)litA','hellitä'),
			('mm','(.*m)mitA','lämmitä'),
			('t','(.*t)OtA','peitota'),
			('p','(.*p)UtA','silputa'),
			('v','(.*)vUtA','vivuta'),
			('>k','(.*)itA','keritä')]),
	('juoruta', 'ws', [(None,'(.*U)tA','juoruta'),
			('mm','(.*m)mUtA','kummuta'),
			('t','(.*t)UtA','luututa'),
			('p','(.*p)UtA','ryöpytä'),
			('k','(.*k)UtA','takuta'),
			('v','(.*)vUtA','kavuta')]),
	('salata', 'ws', [(None,'(.*)AtA','salata'),
	                    ('ng','(.*n)gAtA','hangata'),
			('mm','(.*m)mAtA','kammata'),
			('rr','(.*r)rAtA','kerrata'),
			('nn','(.*n)nAtA','suunnata'),
			('ll','(.*l)lAtA','vallata'),
			('b','(.*b)AtA','lobata'),
			('g','(.*g)AtA','digata'),
			('v','(.*)vAtA','kelvata'),
			('t','(.*t)AtA','kuitata'),
			('d','(.*)dAtA','ladata'),
			('j>k','(.*)jAtA','peljätä'),
			('k','(.*k)AtA','pakata'),
			('p','(.*p)AtA','pompata'),
			('>k','(.*)AtA','taata')]),
	('katketa', 'ws', [(None,'(.*[oeU])tA','katketa'),
	                     ('mm','(.*m)metA','kammeta'),
			 ('ng','(.*n)getA','langeta'),
			 ('t','(.*t)OtA','lotota'),
			 ('k','(.*k)etA','poiketa'),
			 ('v','(.*)vetA','ruveta'),
			 ('d','(.*)detA','todeta'),
			 ('j>k','(.*)jetA','lohjeta'),
			 ('>k','(.*)OtA','saota'),
			 ('>k','(.*)etA','poiketa'),
			 ('ll','(.*l)lOtA','aallota')]),
	('kohota', 'ws', [(None,'(.*[OU])tA','kohota'),
	                    ('rr','(.*r)rOtA','irrota'),
			('mm','(.*m)mOtA','kimmota'),
			('ng','(.*n)gOtA','lingota'),
			('t','(.*t)OtA','netota'),
			('p','(.*p)OtA','upota'),
			('v','(.*r)vOtA','turvota'),
			('k','(.*Vk)OtA','laota'),
			('k','(.*Vk)UtA','takuta'),
			('d','(.*)dOtA','kadota'),
			('>k','(.*)OtA','laota')]),
	('kihistä', '-', [(None,'(.*C)istA','kihistä')]),
	('kitistä', '-', [(None,'(.*C)istA','kitistä')]),
	('taitaa', '-', [(None,'(.*)tAA','taitaa')]),
	('juosta', '-', [(None,'(.*V)stA','juosta')]),
	('nähdä', '-', [(None,'(.*)hdA','nähdä')]),
	('kevetä', '-', [(None,'(.*)vetA','kevetä')]),
        ('haastaa', '-', [(None,'(.*C)AA','haastaa')]), # Historical inflection (Nykysuomen sanakirja, verb type 10).
	('antautua', '-', [(None,'(.*)tUA','antautua')])  # Historical inflection (Nykysuomen sanakirja, verb type 44).
	]

def compileClassmapREs(inputClassmap):
	"""Converts a classmap to a form where regular expressions have been
	compiled to regular expression objects"""
	outputClassmap = []
	for joClass in inputClassmap:
		ruleList = []
		for inputRule in joClass[2]:
			pattern = inputRule[1]
			pattern = pattern.replace('V', '(?:a|á|e|i|o|u|y|ä|ö|é)')
			pattern = pattern.replace('C', '(?:b|c|d|f|g|h|j|k|l|m|n|p|q|r|s|t|v|w|x|y|z|š|ž)')
			pattern = pattern.replace('A', '(?:a|ä)')
			pattern = pattern.replace('O', '(?:o|ö)')
			pattern = pattern.replace('U', '(?:u|y)')
			regExp = re.compile('^' + pattern + '$', re.IGNORECASE)
			outputRule = (inputRule[0], regExp, inputRule[2])
			if len(inputRule) == 4:
				outputRule = (inputRule[0], regExp, inputRule[2], inputRule[3])
			ruleList.append(outputRule)
		outputClassmap.append((joClass[0], joClass[1], ruleList))
	return outputClassmap

def match_re(string, regExp):
	match = regExp.match(string)
	if match == None: return None
	else: return match.group(1)
