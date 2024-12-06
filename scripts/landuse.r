library(tidyverse)

landuse <- read.csv("../input/catchment_characteristics/catch_landuse(NMD).csv") %>% mutate(
  Hällmark = Övrig.öppen.mark.utan.vegetation,
  Hedmark = Övrig.öppen.mark.med.vegetation,
  Hårdgjorda.ytor = Exploaterad.mark..byggnad,
  Semiurbant = Exploaterad.mark..ej.byggnad.eller.väg.järnväg + Exploaterad.mark..väg.järnväg,
  Tallskog = Tallskog..utanför.våtmark.,
  Gran_barrblandskog = Granskog..utanför.våtmark. + Barrblandskog..utanför.våtmark.,
  Blandskog = Lövblandad.barrskog..utanför.våtmark.,
  Lövskog = Triviallövskog..utanför.våtmark. + Ädellövskog..utanför.våtmark. + Triviallövskog.med.ädellövinslag..utanför.våtmark.,
  Ungskog = Temporärt.ej.skog..utanför.våtmark.,
  Skog.på.våtmark = Tallskog..på.våtmark. +
  Granskog..på.våtmark.+
  Barrblandskog..på.våtmark. +
  Lövblandad.barrskog..på.våtmark.+
  Triviallövskog..på.våtmark.+
  Ädellövskog..på.våtmark.+
  Triviallövskog.med.ädellövinslag..på.våtmark.+
  Temporärt.ej.skog..på.våtmark.
  )%>% select(Ingen.täckning,mvm_id,Öppen.våtmark, Åkermark, Hällmark, Hedmark, Hårdgjorda.ytor, Semiurbant, Sjö.och.vattendrag, Tallskog, Gran_barrblandskog, Blandskog, Lövskog, Ungskog, Skog.på.våtmark)

landuse %>% write_csv("../input/catchment_characteristics/PLC8_landuse.csv")
