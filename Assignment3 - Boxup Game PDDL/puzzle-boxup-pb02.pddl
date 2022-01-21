(define (problem eight-puzzle)
  (:domain sliding-tile)
  (:objects
     tile 
     red-block blue-block
     row1 row2 row3 
     col1 col2 col3
     miss-up miss-down miss-left miss-right
     )
  (:init
    (next-row row1 row2)          (next-column col1 col2)
    (next-row row2 row3)     	   (next-column col2 col3) 
    (tile-at tile row2 col2)   
    (is-blank row1 col1)  
    (is-blank row1 col2)
    (is-blank row1 col3)
    ;(is-blank row2 col1)
    (is-blank row2 col2)
    ;(is-blank row2 col3)
    (is-blank row3 col1)
    (is-blank row3 col2)
    (is-blank row3 col3)
    (block-at red-block row2 col3)
    (block-missing red-block miss-left)
    (block-at blue-block row2 col1)
    (block-missing blue-block miss-up)
    (is-tile tile)
    (is-block red-block)
    (is-small-block red-block)
    (is-block blue-block)
    (is-big-block blue-block)
    (is-miss-left miss-left)
    (is-miss-right miss-right)
    (is-miss-up miss-up)
    (is-miss-down miss-down)
    )
  (:goal
    (or
    (and (block-at blue-block row1 col1) (block-at red-block row1 col1))
    (and (block-at blue-block row1 col2) (block-at red-block row1 col2))
    (and (block-at blue-block row1 col3) (block-at red-block row1 col3))   
    (and (block-at blue-block row2 col1) (block-at red-block row2 col1))   
    (and (block-at blue-block row2 col2) (block-at red-block row2 col2))   
    (and (block-at blue-block row2 col3) (block-at red-block row2 col3)) 
    (and (block-at blue-block row3 col1) (block-at red-block row3 col1))   
    (and (block-at blue-block row3 col2) (block-at red-block row3 col2))   
    (and (block-at blue-block row3 col3) (block-at red-block row3 col3))))       
)
