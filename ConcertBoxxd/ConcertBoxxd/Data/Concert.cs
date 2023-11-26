using System.Runtime.CompilerServices;

namespace ConcertBoxxd.Data
{
    public class Concert
    {
        public int ID { get; set; }
        public string Date { get; set; }
        public string Artist{ get; set; }
        public string Tour{ get; set; }
        public string City{ get; set; }
        public string State{ get; set; }
        public string Venue{ get; set; }

        public Concert() { }
        public Concert(int iD, string date, string artist, string tour, string city, string state, string venue)
        {
            ID = iD;
            Date = date;
            Artist = artist;
            Tour = tour;
            City = city;
            State = state;
            Venue = venue;
        }
    }


    //might have to add a ToString override
}
