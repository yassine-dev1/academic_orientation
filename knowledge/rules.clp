;; Règle unique pour l'ingénierie (test)
(defrule main-rule
   (grade (subject math) (value ?math))
   (grade (subject physics) (value ?physics))
   =>
   (bind ?score (+ ?math ?physics))
   (assert (recommendation (domain Ingenierie) (score ?score)))
   (printout t "Score ingenierie: " ?score crlf))