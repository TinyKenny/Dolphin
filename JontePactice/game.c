#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>


//spelet
int main()
{
    int score = 0;
    _Bool snacks = false;
    char c;
    printf ("You see another player: [JMPi]xX420sm0k3r360Xx\n do you attack? (y/n)");
    c = getchar();

    if (c == 'y' || c == 'Y')
    {
        score += 100;
        printf ("You 360 noscope the scrub in the head: he got completely rekt. you now have %d %s", score, "points\n");
    }
    else if (c == 'n' || c == 'N')
    {
        snacks = true;
        printf ("You don't attack. Instead, you decide to leave the game to go and get some FountainView and Doritos\n");
    }
    else
    {
        printf ("You fail!");
        return 0;
    }

    if (snacks == true)
   /* du behöver inte skriva
   if(snacks == true)
   eftersom att (snacks == true) retunerar 1 eller 0 och
   snacks
   är 1 eller 0

   quick fix:
   if(snacks)
   ska det stå istället för
   if(snacks == true) */
    {
        printf ("You have snacks");
    }
    else if (snacks == false)//det går att göra likande saker här men vi tar det sen
    {
        printf ("You don't have snacks");
    }
    else
    {
        printf ("somethings wrong...");
    }
    return 0;

}





