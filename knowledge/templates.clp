;; Templates CLIPS pour le système expert d'orientation

(deftemplate grade
   (slot subject (type SYMBOL))
   (slot value (type INTEGER) (range 0 20)))

(deftemplate preference
   (slot category (type SYMBOL))
   (slot value (type STRING)))

(deftemplate quality
   (slot name (type SYMBOL))
   (slot level (type INTEGER) (default 3)))

(deftemplate recommendation
   (slot domain (type SYMBOL))
   (slot score (type FLOAT))
   (slot confidence (type INTEGER))
   (slot reasoning (type STRING)))